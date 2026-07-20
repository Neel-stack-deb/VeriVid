import re
from app.ai.clients.vision_client import VisionClient
from app.ai.schemas.vision_request import VisionRequest
from app.ai.prompts.builders.vision_prompt_builder import VisionPromptBuilder
from app.schemas.scene import (
    DetectedObject,
    Scene,
    VisibleText,
)
from app.schemas.scene_collection import SceneCollection
from app.schemas.video_artifacts import VideoArtifacts
from app.services.scene_persistence_service import (
    ScenePersistenceService,
)

class VisionService:

    def __init__(
        self,
        vision_client: VisionClient,
    ):
        self._vision_client = vision_client

    def process(
        self,
        artifacts: VideoArtifacts,
    ) -> VideoArtifacts:

        scene_collection = SceneCollection()

        prompt = VisionPromptBuilder.build()

        for frame_path in artifacts.frame_paths:

            request = VisionRequest(
                frame_path=frame_path,
                prompt=prompt,
            )

            result = self._vision_client.analyze(request)

            scene = Scene(
                timestamp=self._extract_timestamp(frame_path),
                frame_path=frame_path,
                description=result.description,
                objects=[
                    DetectedObject(name=obj)
                    for obj in result.objects
                ],
                visible_text=[
                    VisibleText(text=text)
                    for text in result.visible_text
                ],
            )

            scene_collection.scenes.append(scene)

        artifacts.scene_collection = scene_collection

        ScenePersistenceService.save(
            artifacts.workspace,
            scene_collection,
        )

        return artifacts
    
    @staticmethod
    def _extract_timestamp(frame_path):
        match = re.search(r"(\d+)", frame_path.stem)

        if match is None:
            raise ValueError(
                f"Invalid frame name: {frame_path.name}"
            )

        return float(match.group(1))