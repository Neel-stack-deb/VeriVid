from app.schemas.video_artifacts import VideoArtifacts
from app.services.frame_service import FrameService
from app.services.metadata_service import MetadataService
from app.schemas.video_workspace import VideoWorkspace


class VideoPipeline:

    @staticmethod
    def process(workspace : VideoWorkspace) -> VideoArtifacts:

        artifacts = VideoArtifacts(
            workspace=workspace
        )

        artifacts = MetadataService.process(artifacts)
        artifacts = FrameService.process(artifacts)

        return artifacts