from __future__ import annotations

import re
from pathlib import Path
from uuid import UUID

from app.core.constants import VIDEOS_DIR
from app.schemas.video_workspace import VideoWorkspace

_VIDEO_ID_PATTERN = re.compile(
  r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
  re.IGNORECASE,
)


class VideoWorkspaceNotFoundError(Exception):
  pass


class VideoWorkspaceRepository:
  """Resolves workspaces by video_id under the configured videos directory."""

  @staticmethod
  def is_valid_video_id(video_id: str) -> bool:
    if not _VIDEO_ID_PATTERN.match(video_id):
      return False
    try:
      UUID(video_id)
    except ValueError:
      return False
    return True

  @staticmethod
  def workspace_root(video_id: str) -> Path:
    if not VideoWorkspaceRepository.is_valid_video_id(video_id):
      raise VideoWorkspaceNotFoundError(f"Invalid video id: {video_id}")
    root = (VIDEOS_DIR / video_id).resolve()
    videos_root = VIDEOS_DIR.resolve()
    if videos_root not in root.parents and root != videos_root:
      raise VideoWorkspaceNotFoundError("Invalid workspace path")
    if not root.is_dir():
      raise VideoWorkspaceNotFoundError(f"Video not found: {video_id}")
    return root

  @classmethod
  def get_workspace(cls, video_id: str) -> VideoWorkspace:
    root = cls.workspace_root(video_id)
    video_files = list(root.glob("original.*"))
    if not video_files:
      raise VideoWorkspaceNotFoundError(f"Video file missing for {video_id}")
    video_path = video_files[0]

    return VideoWorkspace(
      video_id=video_id,
      root=root,
      video_path=video_path,
      frames_dir=root / "frames",
      metadata_dir=root / "metadata",
      audio_dir=root / "audio",
      transcript_dir=root / "transcripts",
      report_dir=root / "reports",
      scenes_dir=root / "scenes",
      knowledge_dir=root / "knowledge",
      debate_dir=root / "debates",
    )