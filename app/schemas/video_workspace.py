from pathlib import Path
from pydantic import BaseModel


class VideoWorkspace(BaseModel):
    video_id: str

    root: Path

    video_path: Path

    frames_dir: Path
    metadata_dir: Path
    audio_dir: Path
    transcript_dir: Path
    report_dir: Path
    scenes_dir: Path