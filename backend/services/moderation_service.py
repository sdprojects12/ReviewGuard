"""Core review moderation logic.

Per PROJECT_RULES.md: the AI moderates wording, intent, and safety — never
grammar, spelling, capitalization, emojis, slang, or regional English. It
must never change the user's opinion, only preserve meaning while adjusting
tone/wording when needed. Every decision must include an explanation.
"""

from models.review_models import ModerationDecision, ModerationResult
from services.gemini_service import GeminiServiceError, call_gemini

_VALID_DECISIONS = {d.value for d in ModerationDecision}

_PROMPT_TEMPLATE = """You are a review moderation assistant. Moderate the \
review below for wording, intent, and safety only.

Never judge or mention grammar, spelling, capitalization, emojis, slang, \
or regional English. Never change the reviewer's opinion. If an edit is \
suggested, it must preserve the original meaning.

Decision rules:
- "approve": genuine customer experience, respectful criticism, specific \
feedback.
- "needs_adjustment": personal insults, excessive profanity, or overly \
emotional wording. Criticism itself is allowed; only the wording is the \
issue.
- "reject": hate speech, threats, spam, or defamatory accusations \
presented as facts.

Respond with strict JSON only, using exactly these fields and no others:
{{"decision": "approve" | "needs_adjustment" | "reject", "reason": string, \
"suggested_review": string}}

If decision is "approve", suggested_review must equal the original review \
unchanged. Otherwise, suggested_review must be a reworded version that \
preserves the original meaning and opinion.

Review:
\"\"\"{review_text}\"\"\"
"""


class ModerationValidationError(Exception):
    """Raised when the input review text is invalid."""


def moderate_review(review_text):
    """Moderate a single review and return a structured result.

    Args:
        review_text: The raw review text submitted by the user.

    Returns:
        ModerationResult: The decision, reason, and suggested review.

    Raises:
        ModerationValidationError: If review_text is empty/whitespace.
        GeminiServiceError: If the Gemini call fails or returns malformed
            output.
    """
    if not review_text or not review_text.strip():
        raise ModerationValidationError("Review text must not be empty.")

    prompt = _PROMPT_TEMPLATE.format(review_text=review_text.strip())
    raw_result = call_gemini(prompt)

    return _to_moderation_result(raw_result, review_text.strip())


def _to_moderation_result(raw_result, original_review_text):
    """Validate and convert Gemini's raw JSON into a ModerationResult.

    Guards against the model inventing fields or returning an invalid
    decision value, per PROJECT_RULES.md prompt rules.

    Args:
        raw_result: dict parsed from the Gemini response.
        original_review_text: The original trimmed review text, used as a
            fallback if the model omits suggested_review.

    Returns:
        ModerationResult

    Raises:
        GeminiServiceError: If required fields are missing or invalid.
    """
    decision_value = raw_result.get("decision")
    reason = raw_result.get("reason")
    suggested_review = raw_result.get("suggested_review")

    if decision_value not in _VALID_DECISIONS:
        raise GeminiServiceError(
            f"Gemini returned an invalid decision: {decision_value!r}"
        )
    if not reason or not isinstance(reason, str):
        raise GeminiServiceError("Gemini response is missing a valid reason.")
    if not suggested_review or not isinstance(suggested_review, str):
        suggested_review = original_review_text

    return ModerationResult(
        decision=ModerationDecision(decision_value),
        reason=reason.strip(),
        suggested_review=suggested_review.strip(),
    )