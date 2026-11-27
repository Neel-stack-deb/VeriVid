from pydantic import BaseModel


class UploadResponse(BaseModel):
  video_id: str
  filename: str
  content_type: str | None
  file_size: int
  storage_path: str