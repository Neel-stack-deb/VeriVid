from pathlib import Path

from app.schemas.video_artifacts import VideoArtifacts
from app.services.metadata_service import MetadataService


class VideoPipeline:

    @staticmethod
    def process(video_path: Path) -> VideoArtifacts:

        metadata = MetadataService.extract(video_path)

        return VideoArtifacts(
            video_path=video_path,
            metadata=metadata,
        )