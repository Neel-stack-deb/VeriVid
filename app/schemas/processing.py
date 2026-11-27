from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProcessingLifecycleStatus(str, Enum):
  UPLOADED = "uploaded"
  QUEUED = "queued"
  PROCESSING = "processing"
  COMPLETED = "completed"
  FAILED = "failed"


class ProcessingStage(str, Enum):
  """Pipeline stages reflected during execution."""

  METADATA = "metadata"
  FRAMES = "frames"
  AUDIO = "audio"
  TRANSCRIPTION = "transcription"
  VISION = "vision"
  KNOWLEDGE = "knowledge"
  DEBATE = "debate"


class ProcessingRecord(BaseModel):
  video_id: str
  status: ProcessingLifecycleStatus = ProcessingLifecycleStatus.UPLOADED
  current_stage: ProcessingStage | None = None
  progress: float | None = Field(
    default=None,
    ge=0.0,
    le=1.0,
    description="Optional coarse progress; omitted when not measurable.",
  )
  original_filename: str | None = None
  content_type: str | None = None
  file_size: int | None = None
  error: str | None = None
  created_at: datetime = Field(default_factory=datetime.utcnow)
  started_at: datetime | None = None
  completed_at: datetime | None = None