"""Thin client for calling the Gemini API.

Per PROJECT_RULES.md prompt rules: never ask Gemini for markdown, always
request JSON, never allow it to invent new fields, keep prompts concise.
"""

import json

import requests

from config import Config


class GeminiServiceError(Exception):
    """Raised when the Gemini API call fails or returns unusable output."""


def call_gemini(prompt):
    """Send a prompt to Gemini and return the parsed JSON response.

    Forces JSON-only output via responseMimeType so the model cannot wrap
    the answer in markdown or prose.

    Args:
        prompt: The concise instruction/content string to send.

    Returns:
        dict: Parsed JSON object returned by the model.

    Raises:
        GeminiServiceError: If the request fails or the response is not
            valid JSON.
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
        },
    }
    headers = {"Content-Type": "application/json"}
    params = {"key": Config.GEMINI_API_KEY}

    try:
        response = requests.post(
            Config.GEMINI_API_URL,
            params=params,
            headers=headers,
            data=json.dumps(payload),
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GeminiServiceError(f"Gemini API request failed: {exc}") from exc

    return _extract_json(response.json())


def _extract_json(raw_response):
    """Pull the model's JSON text out of the Gemini response envelope.

    Args:
        raw_response: The full decoded JSON body from the Gemini API.

    Returns:
        dict: The model's structured output.

    Raises:
        GeminiServiceError: If the expected fields are missing or the
            text is not valid JSON.
    """
    try:
        text = raw_response["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        raise GeminiServiceError(
            f"Unexpected Gemini response format: {exc}"
        ) from exc