from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class AIProvider(str, Enum):
    FIREWORKS = "fireworks"
    AMD = "amd"


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI_",
        env_file=".env",
        extra="ignore",
    )

    provider: AIProvider = AIProvider.FIREWORKS

    base_url: str

    api_key: str

    timeout: float = 60.0

    models: dict[str, str] = {
        "vision": "Qwen/Qwen2.5-VL-7B-Instruct",
        "debate": "google/gemma-3-12b-it",
        "style": "google/gemma-3-12b-it",
        "chat": "google/gemma-3-12b-it",
    }


ai_settings = AISettings()