from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.schemas.consensus_request import ConsensusRequest
from app.ai.schemas.consensus_response import ConsensusResponse
from app.ai.schemas.context_request import ContextRequest
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.risk_request import RiskRequest
from app.ai.schemas.risk_response import RiskResponse
from app.ai.schemas.verification_request import VerificationRequest
from app.ai.schemas.verification_response import VerificationResponse
from tests.mocks import MockInferenceClient


def _client(
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
  mock_knowledge_base,
) -> MockInferenceClient:
  client = MockInferenceClient()
  client.register(
    ContextResponse,
    ContextResponse(report=mock_context_report),
  )
  client.register(
    VerificationResponse,
    VerificationResponse(report=mock_verification_report),
  )
  client.register(
    RiskResponse,
    RiskResponse(report=mock_risk_report),
  )
  client.register(
    ConsensusResponse,
    ConsensusResponse(report=mock_consensus_report),
  )
  return client


def test_debate_agents_return_reports(
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  client = _client(
    mock_context_report,
    mock_verification_report,
    mock_risk_report,
    mock_consensus_report,
    mock_knowledge_base,
  )

  context = ContextAgent(client).process(
    ContextRequest(knowledge=mock_knowledge_base)
  )
  assert context.report.summary == "Test context summary"

  verification = VerificationAgent(client).process(
    VerificationRequest(
      knowledge=mock_knowledge_base,
      context=context,
    )
  )
  assert verification.report.summary == "Verification complete"

  risk = RiskAgent(client).process(
    RiskRequest(
      knowledge=mock_knowledge_base,
      context=context,
      verification=verification,
    )
  )
  assert risk.report.summary == "Low risk"

  consensus = ConsensusAgent(client).process(
    ConsensusRequest(
      knowledge=mock_knowledge_base,
      context=context,
      verification=verification,
      risk=risk,
    )
  )
  assert consensus.report.summary == "Consensus reached"