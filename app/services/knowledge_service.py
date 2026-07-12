from app.ai.schemas.knowledge_request import KnowledgeRequest


class KnowledgeService:

    def __init__(
        self,
        client,
        persistence_service,
    ):
        self._client = client
        self._persistence = persistence_service

    def process(self, artifacts):

        request = KnowledgeRequest(
            transcript=artifacts.transcript,
            scenes=artifacts.scenes,
        )

        response = self._client.extract(request)

        self._persistence.save(
            artifacts.workspace,
            response.knowledge,
        )

        artifacts.knowledge = response.knowledge

        return artifacts