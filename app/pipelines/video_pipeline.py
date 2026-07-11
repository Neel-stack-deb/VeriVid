from pathlib import Path

from app.schemas.video_artifacts import VideoArtifacts
from app.services.frame_service import FrameService
from app.services.metadata_service import MetadataService


class VideoPipeline:

    @staticmethod
    def process(video_path: Path) -> VideoArtifacts:

        artifacts = VideoArtifacts(
            video_path=video_path
        )

        artifacts = MetadataService.process(artifacts)
        artifacts = FrameService.process(artifacts)

        return artifacts