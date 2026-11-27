from app.ai.agents.verification_agent import VerificationAgent
from app.ai.graph.debate_state import DebateState, DebateStateUpdate
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.verification_request import VerificationRequest


def verification_node(
  state: DebateState,
  *,
  agent: VerificationAgent,
) -> DebateStateUpdate:
  if state.get("error"):
    return {}

  knowledge = state["knowledge"]
  context_report = state.get("context_report")
  if context_report is None:
    raise ValueError("Verification node requires context_report in state")

  try:
    response = agent.process(
      VerificationRequest(
        knowledge=knowledge,
        context=ContextResponse(report=context_report),
      )
    )
  except Exception as exc:
    return {"error": str(exc)}

  return {"verification_report": response.report}