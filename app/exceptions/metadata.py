from app.exceptions.base import VeriVidException


class MetadataExtractionError(VeriVidException):
    """Raised when metadata extraction fails."""