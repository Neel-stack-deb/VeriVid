# app/exceptions/audio.py

from app.exceptions.base import VeriVidException


class AudioExtractionError(VeriVidException):
    """Raised when audio extraction fails."""