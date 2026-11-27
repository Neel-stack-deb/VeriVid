from unittest.mock import patch

import pytest

from app.ai.schemas.knowledge_extraction_response import KnowledgeExtractionResponse
from app.ai.schemas.transcription_response import TranscriptionResponse
from app.pipelines.video_pipeline import VideoPipeline
from app.schemas.transcript import Transcript
from app.schemas.transcript_segment import TranscriptSegment
from tests.conftest import make_workspace_from_video
from tests.mocks import MockInferenceClient, MockTranscriptionClient, MockVisionClient


@pytest.fixture
def mocked_perception_clients(mock_knowledge_base, mock_transcript):
  transcript_response = TranscriptionResponse(
    transcript=mock_transcript,
    provider="mock",
    latency_ms=1,
  )
  transcription = MockTranscriptionClient(transcript_response)
  vision = MockVisionClient()
  knowledge = MockInferenceClient()
  knowledge.register(
    KnowledgeExtractionResponse,
    KnowledgeExtractionResponse(knowledge=mock_knowledge_base),
  )
  return transcription, vision, knowledge


def test_video_pipeline_integration(
  sample_mp4,
  mocked_perception_clients,
):
  transcription, vision, knowledge = mocked_perception_clients
  workspace = make_workspace_from_video(sample_mp4)

  with (
    patch("app.services.whisper_service.transcription_client", transcription),
    patch("app.pipelines.video_pipeline.vision_client", vision),
    patch("app.pipelines.video_pipeline.reasoning_client", knowledge),
  ):
    artifacts = VideoPipeline.process(workspace)

  assert artifacts.metadata is not None
  assert artifacts.frame_paths
  assert artifacts.audio_path is not None
  assert artifacts.transcript.full_text == "Hello world."
  assert artifacts.scene_collection
  assert artifacts.knowledge.entities[0].name == "Speaker"
  assert (workspace.knowledge_dir / "knowledge.json").exists()