class VeriVidException(Exception):
    """Base exception for the VeriVid application."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)