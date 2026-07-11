from pathlib import Path

from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_path: Path

    language: str | None = None

    return_timestamps: bool = True