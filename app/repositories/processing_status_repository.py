import json
from pathlib import Path

from app.repositories.video_workspace_repository import (
  VideoWorkspaceNotFoundError,
  VideoWorkspaceRepository,
)
from app.schemas.processing import ProcessingRecord


class ProcessingStatusRepository:

  STATUS_FILENAME = "status.json"

  @classmethod
  def status_path(cls, video_id: str) -> Path:
    return VideoWorkspaceRepository.workspace_root(video_id) / cls.STATUS_FILENAME

  @classmethod
  def load(cls, video_id: str) -> ProcessingRecord:
    path = cls.status_path(video_id)
    if not path.exists():
      raise VideoWorkspaceNotFoundError(f"No status for video: {video_id}")
    return ProcessingRecord.model_validate_json(
      path.read_text(encoding="utf-8")
    )

  @classmethod
  def save(cls, record: ProcessingRecord) -> None:
    path = cls.status_path(record.video_id)
    path.write_text(
      record.model_dump_json(indent=2),
      encoding="utf-8",
    )

  @classmethod
  def create_initial(
    cls,
    *,
    video_id: str,
    filename: str,
    content_type: str | None,
    file_size: int,
  ) -> ProcessingRecord:
    record = ProcessingRecord(
      video_id=video_id,
      original_filename=filename,
      content_type=content_type,
      file_size=file_size,
    )
    cls.save(record)
    return record