from pathlib import Path

from pydantic import BaseModel

from app.schemas.video_metadata import VideoMetadata
from app.schemas.video_workspace import VideoWorkspace

class VideoArtifacts(BaseModel):
    workspace: VideoWorkspace
    metadata: VideoMetadata | None = None
    frame_paths: list[Path] = []
    audio_path: Path | None = None
    transcript: str | None = None