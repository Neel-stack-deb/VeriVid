from abc import ABC, abstractmethod
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.ai.schemas.knowledge_extraction_response import KnowledgeExtractionResponse

class KnowledgeClient(ABC):

    @abstractmethod
    def extract(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeExtractionResponse:
        ...