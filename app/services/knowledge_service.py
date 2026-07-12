from app.schemas.video_artifacts import VideoArtifacts
from app.ai.schemas.knowledge_request import KnowledgeRequest 

class KnowledgeService:

    def process(
        self,
        artifacts: VideoArtifacts,
    ) -> VideoArtifacts:

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