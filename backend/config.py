"""Application configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central config object for the Flask app.

    Reads all values from environment variables so no secrets live in code.
    """

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")
    GEMINI_API_URL = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    @classmethod
    def validate(cls):
        """Raise a clear error at startup if required config is missing."""
        if not cls.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )