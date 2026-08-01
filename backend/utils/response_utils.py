"""Standard API response envelope helpers.

Per PROJECT_RULES.md, every API response must follow:
  success -> {"success": true, "data": {...}}
  error   -> {"success": false, "message": "..."}
"""

from flask import jsonify


def success_response(data, status_code=200):
    """Wrap payload data in the standard success envelope.

    Args:
        data: JSON-serializable payload to return under "data".
        status_code: HTTP status code (default 200).

    Returns:
        A Flask response tuple (json body, status_code).
    """
    return jsonify({"success": True, "data": data}), status_code


def error_response(message, status_code=400):
    """Wrap an error message in the standard error envelope.

    Args:
        message: Human-readable error description.
        status_code: HTTP status code (default 400).

    Returns:
        A Flask response tuple (json body, status_code).
    """
    return jsonify({"success": False, "message": message}), status_code