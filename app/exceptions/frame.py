from app.exceptions.base import VeriVidException


class FrameExtractionError(VeriVidException):
    """Raised when frame extraction fails."""