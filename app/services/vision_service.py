from app.ai.clients.vision_client import VisionClient
from app.schemas.video_artifacts import VideoArtifacts


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
        raise NotImplementedError