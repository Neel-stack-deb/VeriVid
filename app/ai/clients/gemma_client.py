from app.ai.clients.base.vllm_client import VLLMClient
from app.ai.clients.llm_client import LLMClient


class GemmaClient(
    VLLMClient,
    LLMClient,
):

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError