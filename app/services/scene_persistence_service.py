import json

from app.schemas.scene_collection import SceneCollection
from app.schemas.video_workspace import VideoWorkspace


class ScenePersistenceService:

    @staticmethod
    def save(
        workspace: VideoWorkspace,
        scenes: SceneCollection,
    ) -> None:

        output = (
            workspace.scenes_directory
            / "scenes.json"
        )

        output.write_text(
            scenes.model_dump_json(indent=4),
            encoding="utf-8",
        )