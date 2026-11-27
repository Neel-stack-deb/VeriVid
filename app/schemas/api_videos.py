from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.debate.consensus_report import ConsensusReport
from app.schemas.debate.context_report import ContextReport
from app.schemas.debate.risk_report import RiskReport
from app.schemas.debate.verification_report import VerificationReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.schemas.processing import (
  ProcessingLifecycleStatus,
  ProcessingRecord,
  ProcessingStage,
)
from app.schemas.scene_collection import SceneCollection
from app.schemas.transcript import Transcript
from app.schemas.video_metadata import VideoMetadata


class VideoUploadResponse(BaseModel):
  video_id: str
  filename: str
  status: ProcessingLifecycleStatus = ProcessingLifecycleStatus.UPLOADED


class VideoUploadLegacyResponse(BaseModel):
  """Legacy ``POST /upload`` shape with added ``video_id``."""

  video_id: str
  filename: str
  content_type: str | None
  file_size: int
  storage_path: str


class ProcessVideoResponse(BaseModel):
  video_id: str
  status: ProcessingLifecycleStatus
  message: str = "Processing started"


class VideoDetailResponse(BaseModel):
  video_id: str
  filename: str | None = None
  content_type: str | None = None
  file_size: int | None = None
  status: ProcessingLifecycleStatus
  current_stage: ProcessingStage | None = None
  duration: float | None = None
  width: int | None = None
  height: int | None = None
  fps: float | None = None
  codec: str | None = None
  created_at: datetime | None = None
  started_at: datetime | None = None
  completed_at: datetime | None = None
  error: str | None = None


class VideoStatusResponse(BaseModel):
  video_id: str
  status: ProcessingLifecycleStatus
  current_stage: ProcessingStage | None = None
  progress: float | None = None
  error: str | None = None
  created_at: datetime | None = None
  started_at: datetime | None = None
  completed_at: datetime | None = None


class VideoResultsResponse(BaseModel):
  video_id: str
  status: ProcessingLifecycleStatus
  metadata: VideoMetadata | None = None
  transcript: Transcript | None = None
  scenes: SceneCollection | None = None
  knowledge: KnowledgeBase | None = None
  context_report: ContextReport | None = None
  verification_report: VerificationReport | None = None
  risk_report: RiskReport | None = None
  consensus_report: ConsensusReport | None = None


class DeleteVideoResponse(BaseModel):
  video_id: str
  deleted: bool = True