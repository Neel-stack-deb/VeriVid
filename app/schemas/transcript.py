from pydantic import BaseModel

from app.schemas.transcript_segment import TranscriptSegment


class Transcript(BaseModel):
    language: str

    full_text: str

    segments: list[TranscriptSegment]