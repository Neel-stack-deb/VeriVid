from openai import OpenAI

from app.core.ai_settings import ai_settings


class VLLMClient:

    def __init__(self):
        self._client = OpenAI(
            base_url=ai_settings.base_url,
            api_key=ai_settings.api_key,
            timeout=ai_settings.timeout,
        )

    @property
    def client(self) -> OpenAI:
        return self._client