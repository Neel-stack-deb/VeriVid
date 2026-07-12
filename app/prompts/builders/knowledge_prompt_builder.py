from app.ai.schemas.knowledge_request import KnowledgeRequest

class KnowledgePromptBuilder:

    @staticmethod
    def build(
        request: KnowledgeRequest,
    ) -> str:

        ...