from transformers import pipeline
from app.core.config import settings
from app.ai.clients.transcription_client import TranscriptionClient
from app.ai.schemas.transcription_request import TranscriptionRequest
from app.ai.schemas.transcription_response import TranscriptionResponse

from app.schemas.transcript import Transcript
from app.schemas.transcript_segment import TranscriptSegment


class WhisperTranscriptionClient(TranscriptionClient):

    def __init__(self):

        self.pipeline = pipeline(
            task="automatic-speech-recognition",
            model=settings.whisper_model,
        )

    def transcribe(
        self,
        request: TranscriptionRequest,
    ) -> TranscriptionResponse:

        result = self.pipeline(
            str(request.audio_path),
            return_timestamps=True,
        )

        segments = []

        for chunk in result["chunks"]:

            start, end = chunk["timestamp"]

            segments.append(
                TranscriptSegment(
                    start=start,
                    end=end,
                    text=chunk["text"].strip(),
                )
            )

        transcript = Transcript(
            language=result.get("language", "unknown"),
            full_text=result["text"].strip(),
            segments=segments,
        )

        return TranscriptionResponse(
            transcript=transcript,
            provider="huggingface-whisper",
            latency_ms=0,
        )