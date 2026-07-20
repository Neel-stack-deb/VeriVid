from app.ai.providers.openai_compatible_client import (
    OpenAICompatibleClient,
)
from app.core.config import settings


class AMDClient(OpenAICompatibleClient):

    def __init__(self):

        super().__init__(
            base_url=settings.amd.base_url,
            api_key=settings.amd.api_key,
        )

    def _provider_name(self) -> str:

        return "AMD"