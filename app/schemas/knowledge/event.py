from pydantic import BaseModel

class Event(BaseModel):
    id: str
    title: str
    description: str
    timestamp: float | None = None
    participant_ids: list[str] = []
    confidence: float