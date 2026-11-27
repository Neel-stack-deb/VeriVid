import json
from unittest.mock import patch

import pytest

from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.schemas.consensus_response import ConsensusResponse
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.knowledge_extraction_response import KnowledgeExtractionResponse
from app.ai.schemas.risk_response import RiskResponse
from app.ai.schemas.transcription_response import TranscriptionResponse
from app.ai.schemas.verification_response import VerificationResponse
from app.pipelines.debate_pipeline import DebatePipeline
from app.pipelines.video_pipeline import VideoPipeline
from app.services.debate_persistence_service import DebatePersistenceService
from tests.conftest import make_workspace_from_video
from tests.mocks import MockInferenceClient, MockTranscriptionClient, MockVisionClient


def test_end_to_end_mocked_workflow(
  sample_mp4,
  mock_transcript,
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  workspace = make_workspace_from_video(sample_mp4)

  perception_inference = MockInferenceClient()
  perception_inference.register(
    KnowledgeExtractionResponse,
    KnowledgeExtractionResponse(knowledge=mock_knowledge_base),
  )

  debate_inference = MockInferenceClient()
  debate_inference.register(
    ContextResponse,
    ContextResponse(report=mock_context_report),
  )
  debate_inference.register(
    VerificationResponse,
    VerificationResponse(report=mock_verification_report),
  )
  debate_inference.register(RiskResponse, RiskResponse(report=mock_risk_report))
  debate_inference.register(
    ConsensusResponse,
    ConsensusResponse(report=mock_consensus_report),
  )

  transcription = MockTranscriptionClient(
    TranscriptionResponse(
      transcript=mock_transcript,
      provider="mock",
      latency_ms=1,
    )
  )
  vision = MockVisionClient()

  with (
    patch("app.services.whisper_service.transcription_client", transcription),
    patch("app.pipelines.video_pipeline.vision_client", vision),
    patch("app.pipelines.video_pipeline.reasoning_client", perception_inference),
  ):
    video_artifacts = VideoPipeline.process(workspace)

  debate_pipeline = DebatePipeline(
    context_agent=ContextAgent(debate_inference),
    verification_agent=VerificationAgent(debate_inference),
    risk_agent=RiskAgent(debate_inference),
    consensus_agent=ConsensusAgent(debate_inference),
    persistence_service=DebatePersistenceService,
  )
  debate_artifacts = debate_pipeline.process(workspace, video_artifacts.knowledge)

  expected_files = {
    workspace.metadata_dir / "metadata.json",
    workspace.audio_dir / "audio.wav",
    workspace.transcript_dir / "transcript.json",
    workspace.scenes_dir / "scenes.json",
    workspace.knowledge_dir / "knowledge.json",
    workspace.debate_dir / "context.json",
    workspace.debate_dir / "verification.json",
    workspace.debate_dir / "risk.json",
    workspace.debate_dir / "consensus.json",
  }

  for path in expected_files:
    assert path.exists(), f"Missing artifact: {path}"

  consensus = json.loads(
    (workspace.debate_dir / "consensus.json").read_text(encoding="utf-8")
  )
  assert consensus["summary"] == "Consensus reached"
  assert debate_artifacts.consensus_report.summary == "Consensus reached"