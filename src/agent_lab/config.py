"""Configuration for the direct Model Studio call."""

import os
from dataclasses import dataclass

MODEL_NAME = "qwen3.8-flash"
BASE_URL = "https://ws-nnpvwzj2vhzbu3i6.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
CREDENTIAL_VARIABLE = "DASHSCOPE_API_KEY"
TIMEOUT_SECONDS = 30


class ConfigurationError(Exception):
    """Raised when required local model configuration is missing."""


@dataclass(frozen=True)
class ModelSettings:
    """Settings required to make one direct model request."""

    model: str
    base_url: str
    api_key: str
    timeout_seconds: int


def load_settings(api_key: str | None = None) -> ModelSettings:
    """Load settings without printing or persisting the credential."""

    resolved_key = api_key if api_key is not None else os.getenv(CREDENTIAL_VARIABLE)
    if resolved_key is None or not resolved_key.strip():
        raise ConfigurationError(f"Missing required environment variable: {CREDENTIAL_VARIABLE}")
    return ModelSettings(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=resolved_key,
        timeout_seconds=TIMEOUT_SECONDS,
    )
