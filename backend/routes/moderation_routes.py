"""Routes for review moderation."""

from flask import Blueprint, request

from services.gemini_service import GeminiServiceError
from services.moderation_service import (
    ModerationValidationError,
    moderate_review,
)
from utils.response_utils import error_response, success_response

moderation_bp = Blueprint("moderation", __name__, url_prefix="/api")


@moderation_bp.route("/moderate-review", methods=["POST"])
def moderate_review_endpoint():
    """Moderate a submitted review and return the AI's decision.

    Expects JSON body: {"review_text": "..."}

    Returns:
        200 with {success, data: {decision, reason, suggested_review}}
        400 for invalid/empty input
        502 if the Gemini call fails or returns malformed output
    """
    body = request.get_json(silent=True) or {}
    review_text = body.get("review_text", "")

    try:
        result = moderate_review(review_text)
    except ModerationValidationError as exc:
        return error_response(str(exc), status_code=400)
    except GeminiServiceError as exc:
        return error_response(str(exc), status_code=502)

    return success_response(result.to_dict())