"""Request construction and response handling for one model call."""

from collections.abc import Mapping
from typing import Any

from agent_lab.config import ModelSettings


class TransportError(Exception):
    """Raised when the provider request cannot be completed."""


class ResponseFormatError(Exception):
    """Raised when the provider response does not contain text content."""


def build_request(settings: ModelSettings, user_input: str) -> dict[str, Any]:
    """Build one OpenAI-compatible chat request from CLI input."""

    return {
        "method": "POST",
        "url": f"{settings.base_url}/chat/completions",
        "timeout_seconds": settings.timeout_seconds,
        "headers": {
            "Authorization": f"Bearer {settings.api_key}",
            "Content-Type": "application/json",
        },
        "json": {
            "model": settings.model,
            "messages": [{"role": "user", "content": user_input}],
        },
    }


def extract_text(response: Mapping[str, Any]) -> str:
    """Extract the first text response without making another model call."""

    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ResponseFormatError("Model response does not contain text content.") from error
    if not isinstance(content, str) or not content.strip():
        raise ResponseFormatError("Model response does not contain text content.")
    return content


def run_once(settings: ModelSettings, user_input: str, transport) -> str:
    """Send one input through the supplied transport and return its text."""

    try:
        response = transport(build_request(settings, user_input))
    except TransportError:
        raise
    except Exception as error:
        raise TransportError("Model request failed.") from error
    return extract_text(response)
