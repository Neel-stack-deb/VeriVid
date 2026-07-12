from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.ai.schemas.knowledge_extraction_response import KnowledgeExtractionResponse
from app.ai.clients.knowledge_client import KnowledgeClient

class GemmaKnowledgeClient(KnowledgeClient):

    def extract(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeExtractionResponse:

        # Build prompt
        # Call inference endpoint
        # Parse JSON
        # Return KnowledgeResponse

        ...