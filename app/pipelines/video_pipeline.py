from app.schemas.video_artifacts import VideoArtifacts
from app.services.frame_service import FrameService
from app.services.metadata_service import MetadataService
from app.schemas.video_workspace import VideoWorkspace
from app.services.audio_service import AudioService
from app.services.whisper_service import WhisperService

class VideoPipeline:

    @staticmethod
    def process(workspace : VideoWorkspace) -> VideoArtifacts:

        artifacts = VideoArtifacts(
            workspace=workspace
        )

        artifacts = MetadataService.process(artifacts)
        artifacts = FrameService.process(artifacts)
        artifacts = AudioService.process(artifacts)
        artifacts = WhisperService.process(artifacts)

        return artifacts