from app.exceptions.base import VeriVidException


class MediaProcessingError(VeriVidException):
    """Raised when an FFmpeg media operation fails."""