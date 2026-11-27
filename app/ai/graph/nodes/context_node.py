from app.ai.agents.context_agent import ContextAgent
from app.ai.graph.debate_state import DebateState, DebateStateUpdate
from app.ai.schemas.context_request import ContextRequest


def context_node(
  state: DebateState,
  *,
  agent: ContextAgent,
) -> DebateStateUpdate:
  knowledge = state.get("knowledge")
  if knowledge is None:
    raise ValueError("Debate graph requires knowledge in state")

  try:
    response = agent.process(ContextRequest(knowledge=knowledge))
  except Exception as exc:
    return {"error": str(exc)}

  return {"context_report": response.report}