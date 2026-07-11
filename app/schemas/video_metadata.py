from pydantic import BaseModel


class VideoMetadata(BaseModel):
    filename: str
    duration: float
    size: int
    width: int
    height: int
    fps: float
    codec: str