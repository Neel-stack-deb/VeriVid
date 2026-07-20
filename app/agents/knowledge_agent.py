from app.ai.clients.base.inference_client import InferenceClient
from app.ai.schemas.inference_request import InferenceRequest
from app.ai.schemas.knowledge_extraction_response import (
    KnowledgeExtractionResponse,
)
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.core.ai_settings import ai_settings
from app.ai.prompts.builders.knowledge_prompt_builder import (
    KnowledgePromptBuilder,
)

from app.agents.base_agent import BaseAgent


class KnowledgeAgent(BaseAgent):

    def __init__(
        self,
        reasoning_client: InferenceClient,
    ):
        super().__init__(reasoning_client)

    def extract(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeExtractionResponse:

        prompt = KnowledgePromptBuilder.build(request)

        inference_request = InferenceRequest(
            model=ai_settings.models["debate"],
            system_prompt="",
            user_prompt=prompt,
            response_model=KnowledgeExtractionResponse,
        )

        self._reasoning_client.generate(inference_request)

        raise NotImplementedError