from pydantic import BaseModel

from app.schemas.transcript import Transcript


class TranscriptionResponse(BaseModel):
    transcript: Transcript

    provider: str

    latency_ms: float