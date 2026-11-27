import io

import pytest
from fastapi import UploadFile

from app.services.workspace_service import WorkspaceService


@pytest.mark.asyncio
async def test_workspace_creates_expected_directories(tmp_video_dir, sample_mp4):
  upload = UploadFile(
    filename="sample.mp4",
    file=io.BytesIO(sample_mp4.read_bytes()),
    headers={"content-type": "video/mp4"},
  )

  workspace, size = await WorkspaceService.create(upload)

  assert size > 0
  assert workspace.video_path.exists()
  for directory in (
    workspace.frames_dir,
    workspace.metadata_dir,
    workspace.audio_dir,
    workspace.transcript_dir,
    workspace.scenes_dir,
    workspace.knowledge_dir,
    workspace.debate_dir,
  ):
    assert directory.is_dir()