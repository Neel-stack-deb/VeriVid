from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def tmp_video_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
  """Isolate workspace storage under a temporary data directory."""
  data_dir = tmp_path / "data" / "videos"
  data_dir.mkdir(parents=True)
  monkeypatch.setattr(
    "app.core.constants.VIDEOS_DIR",
    data_dir,
  )
  return data_dir


@pytest.fixture
def sample_mp4(tmp_path: Path) -> Path:
  """Create a minimal valid MP4 via ffmpeg (requires ffmpeg in PATH)."""
  output = tmp_path / "sample.mp4"
  import subprocess

  command = [
    "ffmpeg",
    "-y",
    "-f",
    "lavfi",
    "-i",
    "testsrc=duration=4:size=320x240:rate=1",
    "-f",
    "lavfi",
    "-i",
    "sine=frequency=440:duration=4",
    "-c:v",
    "libx264",
    "-c:a",
    "aac",
    "-shortest",
    str(output),
  ]
  subprocess.run(command, check=True, capture_output=True)
  return output


def make_workspace_from_video(video_path: Path, video_id: str = "test-video-id") -> "VideoWorkspace":
  from shutil import copytree
  from app.schemas.video_workspace import VideoWorkspace

  root = video_path.parent / video_id
  for name in (
    "metadata",
    "frames",
    "audio",
    "transcripts",
    "reports",
    "scenes",
    "knowledge",
    "debates",
  ):
    (root / name).mkdir(parents=True, exist_ok=True)

  dest_video = root / f"original{video_path.suffix}"
  dest_video.write_bytes(video_path.read_bytes())

  return VideoWorkspace(
    video_id=video_id,
    root=root,
    video_path=dest_video,
    frames_dir=root / "frames",
    metadata_dir=root / "metadata",
    audio_dir=root / "audio",
    transcript_dir=root / "transcripts",
    report_dir=root / "reports",
    scenes_dir=root / "scenes",
    knowledge_dir=root / "knowledge",
    debate_dir=root / "debates",
  )


@pytest.fixture
def mock_transcript():
  from app.schemas.transcript import Transcript
  from app.schemas.transcript_segment import TranscriptSegment

  return Transcript(
    language="en",
    full_text="Hello world.",
    segments=[
      TranscriptSegment(start=0.0, end=1.0, text="Hello world."),
    ],
  )


@pytest.fixture
def mock_knowledge_base():
  from app.schemas.knowledge.knowledge_base import KnowledgeBase
  from app.schemas.knowledge.entity import Entity

  return KnowledgeBase(
    entities=[
      Entity(
        id="ent-1",
        name="Speaker",
        type="Person",
        description="A person in the video",
        confidence=0.9,
      )
    ],
  )


@pytest.fixture
def mock_context_report():
  from app.schemas.debate.context_report import ContextReport

  return ContextReport(
    summary="Test context summary",
    confidence=0.85,
    model_name="mock-model",
  )


@pytest.fixture
def mock_verification_report():
  from app.schemas.debate.verification_report import VerificationReport

  return VerificationReport(
    summary="Verification complete",
    confidence=0.8,
    model_name="mock-model",
  )


@pytest.fixture
def mock_risk_report():
  from app.schemas.debate.risk_report import RiskReport

  return RiskReport(
    summary="Low risk",
    confidence=0.75,
    model_name="mock-model",
  )


@pytest.fixture
def mock_consensus_report():
  from app.schemas.debate.consensus_report import ConsensusReport

  return ConsensusReport(
    summary="Consensus reached",
    confidence=0.9,
    model_name="mock-model",
  )