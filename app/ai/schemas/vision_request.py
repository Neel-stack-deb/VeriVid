from pathlib import Path

from pydantic import BaseModel


class VisionRequest(BaseModel):
    frame_path: Path
    prompt: str