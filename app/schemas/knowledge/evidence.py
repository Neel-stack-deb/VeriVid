from pydantic import BaseModel

class Evidence(BaseModel):
    id: str
    type: str
    content: str
    timestamp: float | None = None
    frame_path: str | None = None
    confidence: float