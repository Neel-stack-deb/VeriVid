import json

from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.schemas.video_workspace import VideoWorkspace


class KnowledgePersistenceService:

    @staticmethod
    def save(
        workspace: VideoWorkspace,
        knowledge: KnowledgeBase,
    ) -> None:

        path = workspace.knowledge_dir / "knowledge.json"

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                knowledge.model_dump(),
                file,
                indent=2,
                ensure_ascii=False,
            )