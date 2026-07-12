from app.prompts.builders.knowledge_prompt_builder import KnowledgePromptBuilder
from app.ai.clients.knowledge_client import KnowledgeClient
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.ai.schemas.knowledge_extraction_response import KnowledgeExtractionResponse


class GemmaKnowledgeClient(KnowledgeClient):

    def extract(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeExtractionResponse:

        prompt = KnowledgePromptBuilder.build(request)

        # TODO:
        # response = inference_client.generate(prompt)

        # parsed = ...

        # return KnowledgeResponse(
        #     knowledge=parsed
        # )

        raise NotImplementedError