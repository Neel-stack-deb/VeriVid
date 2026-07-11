from pathlib import Path

from pydantic import BaseModel

from app.schemas.video_metadata import VideoMetadata


class VideoArtifacts(BaseModel):
    video_path: Path
    metadata: VideoMetadata
    frame_paths: list[Path] = []
    audio_path: Path | None = None
    transcript: str | None = None