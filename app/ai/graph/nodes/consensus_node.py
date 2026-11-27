from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.graph.debate_state import DebateState, DebateStateUpdate
from app.ai.schemas.consensus_request import ConsensusRequest
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.risk_response import RiskResponse
from app.ai.schemas.verification_response import VerificationResponse


def consensus_node(
  state: DebateState,
  *,
  agent: ConsensusAgent,
) -> DebateStateUpdate:
  if state.get("error"):
    return {}

  knowledge = state["knowledge"]
  context_report = state.get("context_report")
  verification_report = state.get("verification_report")
  risk_report = state.get("risk_report")
  if (
    context_report is None
    or verification_report is None
    or risk_report is None
  ):
    raise ValueError(
      "Consensus node requires context, verification, and risk reports"
    )

  try:
    response = agent.process(
      ConsensusRequest(
        knowledge=knowledge,
        context=ContextResponse(report=context_report),
        verification=VerificationResponse(report=verification_report),
        risk=RiskResponse(report=risk_report),
      )
    )
  except Exception as exc:
    return {"error": str(exc)}

  return {"consensus_report": response.report}