from app.exceptions.base import VeriVidException


class StorageError(VeriVidException):
    """Raised when a file cannot be stored."""