from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI_",
        env_file=".env",
        extra="ignore",
    )

    base_url: str = Field(
        default="http://localhost:8001/v1"
    )
    
    api_key: str
    timeout: float

    models = {
        "vision": "Qwen/Qwen2.5-VL-7B-Instruct",
        "debate": "google/gemma-3-12b-it",
        "style": "google/gemma-3-12b-it",
        "chat": "google/gemma-3-12b-it",
    }


ai_settings = AISettings()