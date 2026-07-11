from pydantic import BaseModel, Field

from app.schemas.scene import Scene


class SceneCollection(BaseModel):
    scenes: list[Scene] = Field(default_factory=list)