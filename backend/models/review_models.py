"""Data models for the review moderation domain."""

from dataclasses import dataclass
from enum import Enum


class ModerationDecision(str, Enum):
    """The three possible moderation outcomes, per PROJECT_RULES.md.

    Maps directly to the UI colors: Approve=green, Needs Adjustment=yellow,
    Reject=red.
    """

    APPROVE = "approve"
    NEEDS_ADJUSTMENT = "needs_adjustment"
    REJECT = "reject"


@dataclass
class ModerationResult:
    """Structured result of moderating a single review.

    Attributes:
        decision: One of ModerationDecision.
        reason: Plain-language explanation for the decision (transparency
            is required by PROJECT_RULES.md).
        suggested_review: An edited version of the review that preserves
            the original meaning/opinion, or the original text unchanged
            if no edit is needed.
    """

    decision: ModerationDecision
    reason: str
    suggested_review: str

    def to_dict(self):
        """Serialize to a plain dict for the API response."""
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "suggested_review": self.suggested_review,
        }