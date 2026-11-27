from __future__ import annotations

import logging
from fastapi import UploadFile

from app.jobs.executor import InProcessJobExecutor, job_executor
from app.repositories.processing_status_repository import (
  ProcessingStatusRepository,
)
from app.repositories.video_results_repository import VideoResultsRepository
from app.repositories.video_workspace_repository import (
  VideoWorkspaceNotFoundError,
  VideoWorkspaceRepository,
)
from app.schemas.api_videos import (
  DeleteVideoResponse,
  ProcessVideoResponse,
  VideoDetailResponse,
  VideoResultsResponse,
  VideoStatusResponse,
  VideoUploadResponse,
)
from app.schemas.processing import ProcessingLifecycleStatus
from app.services.upload_service import UploadService
from app.services.video_processing_orchestrator import VideoProcessingOrchestrator
from app.services.workspace_service import WorkspaceService

logger = logging.getLogger(__name__)


class VideoApiService:

  def __init__(
    self,
    *,
    orchestrator: VideoProcessingOrchestrator | None = None,
    executor=job_executor,
  ) -> None:
    self._orchestrator = orchestrator or VideoProcessingOrchestrator()
    self._executor = executor

  async def upload_video(self, video: UploadFile) -> VideoUploadResponse:
    legacy = await UploadService.upload(video)
    workspace = VideoWorkspaceRepository.get_workspace(legacy.video_id)
    ProcessingStatusRepository.create_initial(
      video_id=workspace.video_id,
      filename=legacy.filename,
      content_type=legacy.content_type,
      file_size=legacy.file_size,
    )
    return VideoUploadResponse(
      video_id=workspace.video_id,
      filename=legacy.filename,
    )

  def start_processing(self, video_id: str) -> ProcessVideoResponse:
    record = ProcessingStatusRepository.load(video_id)
    if record.status in (
      ProcessingLifecycleStatus.QUEUED,
      ProcessingLifecycleStatus.PROCESSING,
    ):
      return ProcessVideoResponse(
        video_id=video_id,
        status=record.status,
        message="Processing already in progress",
      )

    if record.status == ProcessingLifecycleStatus.COMPLETED:
      return ProcessVideoResponse(
        video_id=video_id,
        status=record.status,
        message="Processing already completed",
      )

    workspace = VideoWorkspaceRepository.get_workspace(video_id)
    record.status = ProcessingLifecycleStatus.QUEUED
    record.error = None
    ProcessingStatusRepository.save(record)

    def _job() -> None:
      logger.info("Starting processing for video_id=%s", video_id)
      try:
        self._orchestrator.run(workspace)
        logger.info("Completed processing for video_id=%s", video_id)
      except Exception:
        logger.exception("Processing failed for video_id=%s", video_id)

    accepted = self._executor.submit(video_id, _job)
    if not accepted:
      record.status = ProcessingLifecycleStatus.PROCESSING
      ProcessingStatusRepository.save(record)
      return ProcessVideoResponse(
        video_id=video_id,
        status=ProcessingLifecycleStatus.PROCESSING,
        message="Processing already in progress",
      )

    record = ProcessingStatusRepository.load(video_id)
    return ProcessVideoResponse(
      video_id=video_id,
      status=record.status,
      message="Processing started",
    )

  def get_status(self, video_id: str) -> VideoStatusResponse:
    record = ProcessingStatusRepository.load(video_id)
    return VideoStatusResponse(
      video_id=record.video_id,
      status=record.status,
      current_stage=record.current_stage,
      progress=record.progress,
      error=record.error,
      created_at=record.created_at,
      started_at=record.started_at,
      completed_at=record.completed_at,
    )

  def get_video_detail(self, video_id: str) -> VideoDetailResponse:
    record = ProcessingStatusRepository.load(video_id)
    results = VideoResultsRepository.load_all(video_id)
    metadata = results.get("metadata")

    return VideoDetailResponse(
      video_id=video_id,
      filename=record.original_filename,
      content_type=record.content_type,
      file_size=record.file_size,
      status=record.status,
      current_stage=record.current_stage,
      duration=metadata.duration if metadata else None,
      width=metadata.width if metadata else None,
      height=metadata.height if metadata else None,
      fps=metadata.fps if metadata else None,
      codec=metadata.codec if metadata else None,
      created_at=record.created_at,
      started_at=record.started_at,
      completed_at=record.completed_at,
      error=record.error,
    )

  def get_results(self, video_id: str) -> VideoResultsResponse:
    record = ProcessingStatusRepository.load(video_id)
    payload = VideoResultsRepository.load_all(video_id)
    return VideoResultsResponse(
      video_id=video_id,
      status=record.status,
      metadata=payload.get("metadata"),
      transcript=payload.get("transcript"),
      scenes=payload.get("scenes"),
      knowledge=payload.get("knowledge"),
      context_report=payload.get("context_report"),
      verification_report=payload.get("verification_report"),
      risk_report=payload.get("risk_report"),
      consensus_report=payload.get("consensus_report"),
    )

  def delete_video(self, video_id: str) -> DeleteVideoResponse:
    if InProcessJobExecutor.is_active(video_id):
      raise RuntimeError("Cannot delete video while processing is active")

    workspace = VideoWorkspaceRepository.get_workspace(video_id)
    WorkspaceService.delete(workspace)
    return DeleteVideoResponse(video_id=video_id)