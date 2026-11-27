import json

from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.schemas.consensus_response import ConsensusResponse
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.risk_response import RiskResponse
from app.ai.schemas.verification_response import VerificationResponse
from app.pipelines.debate_pipeline import DebatePipeline
from app.services.debate_persistence_service import DebatePersistenceService
from tests.conftest import make_workspace_from_video
from tests.mocks import MockInferenceClient


def test_debate_pipeline_persists_four_reports(
  sample_mp4,
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  client = MockInferenceClient()
  client.register(ContextResponse, ContextResponse(report=mock_context_report))
  client.register(
    VerificationResponse,
    VerificationResponse(report=mock_verification_report),
  )
  client.register(RiskResponse, RiskResponse(report=mock_risk_report))
  client.register(
    ConsensusResponse,
    ConsensusResponse(report=mock_consensus_report),
  )

  workspace = make_workspace_from_video(sample_mp4)
  pipeline = DebatePipeline(
    context_agent=ContextAgent(client),
    verification_agent=VerificationAgent(client),
    risk_agent=RiskAgent(client),
    consensus_agent=ConsensusAgent(client),
    persistence_service=DebatePersistenceService,
  )

  artifacts = pipeline.process(workspace, mock_knowledge_base)

  assert artifacts.context_report is not None
  assert artifacts.consensus_report.summary == "Consensus reached"

  for name in (
    "context.json",
    "verification.json",
    "risk.json",
    "consensus.json",
  ):
    path = workspace.debate_dir / name
    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert "summary" in payload