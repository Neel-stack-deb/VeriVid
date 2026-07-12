from pydantic import BaseModel

class Entity(BaseModel):
    id: str
    name: str
    type: str
    description: str | None = None
    confidence: float