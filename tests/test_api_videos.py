import json
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from app.jobs.executor import JobExecutor
from app.repositories.processing_status_repository import (
  ProcessingStatusRepository,
)
from app.repositories.video_workspace_repository import VideoWorkspaceRepository
from app.ai.schemas.consensus_response import ConsensusResponse
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.knowledge_extraction_response import (
  KnowledgeExtractionResponse,
)
from app.ai.schemas.risk_response import RiskResponse
from app.ai.schemas.transcription_response import TranscriptionResponse
from app.ai.schemas.verification_response import VerificationResponse
from app.schemas.processing import ProcessingLifecycleStatus
from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.knowledge_agent import KnowledgeAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.pipelines.debate_pipeline import DebatePipeline
from app.services.debate_persistence_service import DebatePersistenceService
from app.services.video_api_service import VideoApiService
from app.services.video_processing_orchestrator import VideoProcessingOrchestrator
from main import app
from tests.mocks import (
  MockInferenceClient,
  MockTranscriptionClient,
  MockVisionClient,
)


class SyncJobExecutor(JobExecutor):
  def submit(self, video_id: str, fn) -> bool:
    fn()
    return True


@pytest.fixture
def client(tmp_video_dir):
  return TestClient(app)


def _upload(client: TestClient, sample_mp4: Path) -> str:
  with sample_mp4.open("rb") as video:
    response = client.post(
      "/api/videos/upload",
      files={"video": ("sample.mp4", video, "video/mp4")},
    )
  assert response.status_code == 201
  return response.json()["video_id"]


def test_api_upload_returns_video_id(client: TestClient, sample_mp4: Path):
  video_id = _upload(client, sample_mp4)
  assert VideoWorkspaceRepository.is_valid_video_id(video_id)
  record = ProcessingStatusRepository.load(video_id)
  assert record.status == ProcessingLifecycleStatus.UPLOADED


def test_legacy_upload_includes_video_id(client: TestClient, sample_mp4: Path):
  with sample_mp4.open("rb") as video:
    response = client.post(
      "/upload",
      files={"video": ("sample.mp4", video, "video/mp4")},
    )
  assert response.status_code == 200
  assert "video_id" in response.json()


def test_upload_rejects_invalid_extension(client: TestClient):
  response = client.post(
    "/api/videos/upload",
    files={"video": ("bad.txt", b"not-a-video", "text/plain")},
  )
  assert response.status_code == 400


def test_process_and_status(client: TestClient, sample_mp4: Path):
  video_id = _upload(client, sample_mp4)

  class NoOpOrchestrator:
    def run(self, workspace) -> None:
      record = ProcessingStatusRepository.load(workspace.video_id)
      record.status = ProcessingLifecycleStatus.COMPLETED
      ProcessingStatusRepository.save(record)

  with patch("app.api.videos._service", VideoApiService(
    orchestrator=NoOpOrchestrator(),
    executor=SyncJobExecutor(),
  )):
    process = client.post(f"/api/videos/{video_id}/process")
    assert process.status_code == 200

    status = client.get(f"/api/videos/{video_id}/status")
    assert status.status_code == 200
    assert status.json()["status"] == "completed"


def test_duplicate_process_returns_in_progress_message(
  client: TestClient,
  sample_mp4: Path,
):
  video_id = _upload(client, sample_mp4)
  record = ProcessingStatusRepository.load(video_id)
  record.status = ProcessingLifecycleStatus.PROCESSING
  ProcessingStatusRepository.save(record)

  response = client.post(f"/api/videos/{video_id}/process")
  assert response.status_code == 200
  assert "already" in response.json()["message"].lower()


def test_missing_video_returns_404(client: TestClient):
  missing_id = "00000000-0000-4000-8000-000000000000"
  assert client.get(f"/api/videos/{missing_id}/status").status_code == 404


def test_results_partial_before_processing(client: TestClient, sample_mp4: Path):
  video_id = _upload(client, sample_mp4)
  response = client.get(f"/api/videos/{video_id}/results")
  assert response.status_code == 200
  body = response.json()
  assert body["status"] == "uploaded"
  assert body["transcript"] is None


def test_delete_video_removes_workspace(client: TestClient, sample_mp4: Path):
  video_id = _upload(client, sample_mp4)
  root = VideoWorkspaceRepository.workspace_root(video_id)
  assert root.exists()

  deleted = client.delete(f"/api/videos/{video_id}")
  assert deleted.status_code == 200
  assert not root.exists()


def test_background_processing_success(
  client: TestClient,
  sample_mp4: Path,
  mock_transcript,
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  video_id = _upload(client, sample_mp4)

  transcription = MockTranscriptionClient(
    TranscriptionResponse(
      transcript=mock_transcript,
      provider="mock",
      latency_ms=1,
    )
  )
  vision = MockVisionClient()
  inference = MockInferenceClient()
  inference.register(
    KnowledgeExtractionResponse,
    KnowledgeExtractionResponse(knowledge=mock_knowledge_base),
  )
  inference.register(ContextResponse, ContextResponse(report=mock_context_report))
  inference.register(
    VerificationResponse,
    VerificationResponse(report=mock_verification_report),
  )
  inference.register(RiskResponse, RiskResponse(report=mock_risk_report))
  inference.register(
    ConsensusResponse,
    ConsensusResponse(report=mock_consensus_report),
  )

  debate = DebatePipeline(
    context_agent=ContextAgent(inference),
    verification_agent=VerificationAgent(inference),
    risk_agent=RiskAgent(inference),
    consensus_agent=ConsensusAgent(inference),
    persistence_service=DebatePersistenceService,
  )
  orchestrator = VideoProcessingOrchestrator(
    knowledge_agent=KnowledgeAgent(inference),
    debate_pipeline=debate,
  )
  with (
    patch("app.services.whisper_service.transcription_client", transcription),
    patch("app.services.video_processing_orchestrator.vision_client", vision),
    patch(
      "app.api.videos._service",
      VideoApiService(
        orchestrator=orchestrator,
        executor=SyncJobExecutor(),
      ),
    ),
  ):
    assert client.post(f"/api/videos/{video_id}/process").status_code == 200
    for _ in range(50):
      status = client.get(f"/api/videos/{video_id}/status").json()
      if status["status"] in ("completed", "failed"):
        break
      time.sleep(0.05)
    assert status["status"] == "completed"

    results = client.get(f"/api/videos/{video_id}/results").json()
    assert results["knowledge"]["entities"][0]["name"] == "Speaker"
    assert results["consensus_report"]["summary"] == "Consensus reached"