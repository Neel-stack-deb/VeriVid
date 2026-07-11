from pathlib import Path

from pydantic import BaseModel, Field


class DetectedObject(BaseModel):
    name: str
    confidence: float | None = None


class VisibleText(BaseModel):
    text: str


class Scene(BaseModel):
    timestamp: float = Field(
        description="Timestamp of the frame in seconds."
    )
    frame_path: Path
    description: str
    objects: list[DetectedObject] = Field(default_factory=list)
    visible_text: list[VisibleText] = Field(default_factory=list)