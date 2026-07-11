from abc import ABC, abstractmethod

from app.ai.schemas.transcription_request import TranscriptionRequest
from app.ai.schemas.transcription_response import TranscriptionResponse


class TranscriptionClient(ABC):

    @abstractmethod
    def transcribe(
        self,
        request: TranscriptionRequest,
    ) -> TranscriptionResponse:
        """
        Performs speech-to-text transcription.
        """
        pass