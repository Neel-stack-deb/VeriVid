from app.ai.agents.risk_agent import RiskAgent
from app.ai.graph.debate_state import DebateState, DebateStateUpdate
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.risk_request import RiskRequest
from app.ai.schemas.verification_response import VerificationResponse


def risk_node(
  state: DebateState,
  *,
  agent: RiskAgent,
) -> DebateStateUpdate:
  if state.get("error"):
    return {}

  knowledge = state["knowledge"]
  context_report = state.get("context_report")
  verification_report = state.get("verification_report")
  if context_report is None or verification_report is None:
    raise ValueError("Risk node requires context_report and verification_report")

  try:
    response = agent.process(
      RiskRequest(
        knowledge=knowledge,
        context=ContextResponse(report=context_report),
        verification=VerificationResponse(report=verification_report),
      )
    )
  except Exception as exc:
    return {"error": str(exc)}

  return {"risk_report": response.report}