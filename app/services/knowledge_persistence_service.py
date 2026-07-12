from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.schemas.video_workspace import VideoWorkspace

class KnowledgePersistenceService:

    @staticmethod
    def save(
        workspace: VideoWorkspace,
        knowledge: KnowledgeBase,
    ) -> None:

        ...