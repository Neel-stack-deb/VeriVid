from app.ai.analyzers.context_analyzer import ContextAnalyzer
from app.prompts.builders.context_prompt_builder import ContextPromptBuilder
from app.ai.clients.inference_client import InferenceClient
from app.ai.schemas.context_request import ContextRequest
from app.ai.schemas.context_response import ContextResponse
from app.schemas.debate.context_report import ContextReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class GemmaContextAnalyzer(ContextAnalyzer):

    def __init__(
        self,
        client: InferenceClient,
    ):
        self._client = client

    def analyze(
        self,
        data: KnowledgeBase,
    ) -> ContextReport:

        request = ContextRequest(
            knowledge=data,
        )

        prompt = ContextPromptBuilder.build(
            request,
        )

        response = self._client.generate(
            prompt,
            response_model=ContextResponse,
        )

        return response.report