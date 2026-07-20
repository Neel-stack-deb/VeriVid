from app.ai.providers.openai_compatible_client import (
    OpenAICompatibleClient,
)
from app.core.config import settings


class FireworksClient(OpenAICompatibleClient):

    def __init__(self):

        super().__init__(
            base_url=settings.fireworks.base_url,
            api_key=settings.fireworks.api_key,
        )