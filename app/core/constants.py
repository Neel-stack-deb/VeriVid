from pathlib import Path

UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1 MB

MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
}

ALLOWED_VIDEO_MIME_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-matroska",
    "video/webm",
}

FRAME_SAMPLE_INTERVAL = 3  # seconds
UPLOAD_DIRECTORY = Path("data/uploads")