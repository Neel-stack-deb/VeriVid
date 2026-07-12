from pydantic import BaseModel

class Claim(BaseModel):
    id: str
    statement: str
    speaker: str | None = None
    timestamp: float | None = None
    evidence_ids: list[str] = []
    confidence: float