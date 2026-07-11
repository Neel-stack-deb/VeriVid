from pydantic import BaseModel, Field


class FrameVisionResult(BaseModel):
    description: str

    objects: list[str] = Field(default_factory=list)

    visible_text: list[str] = Field(default_factory=list)