from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from langgraph.graph import END, START, StateGraph

from app.ai.graph.debate_state import DebateState
from app.ai.graph.nodes import (
  consensus_node,
  context_node,
  risk_node,
  verification_node,
)
from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.schemas.knowledge.knowledge_base import KnowledgeBase

if TYPE_CHECKING:
  from langgraph.graph.state import CompiledStateGraph

  from app.ai.agents.consensus_agent import ConsensusAgent
  from app.ai.agents.context_agent import ContextAgent
  from app.ai.agents.risk_agent import RiskAgent
  from app.ai.agents.verification_agent import VerificationAgent


class DebateGraphError(Exception):
  """Raised when the debate graph finishes with an error state."""


def build_debate_graph(
  *,
  context_agent: ContextAgent,
  verification_agent: VerificationAgent,
  risk_agent: RiskAgent,
  consensus_agent: ConsensusAgent,
) -> CompiledStateGraph:
  """
  Compile a sequential LangGraph for the debate council.

  Agents are injected at graph build time; they are not part of graph state.
  """
  graph = StateGraph(DebateState)

  graph.add_node(
    "context",
    partial(context_node, agent=context_agent),
  )
  graph.add_node(
    "verification",
    partial(verification_node, agent=verification_agent),
  )
  graph.add_node(
    "risk",
    partial(risk_node, agent=risk_agent),
  )
  graph.add_node(
    "consensus",
    partial(consensus_node, agent=consensus_agent),
  )

  graph.add_edge(START, "context")
  graph.add_edge("context", "verification")
  graph.add_edge("verification", "risk")
  graph.add_edge("risk", "consensus")
  graph.add_edge("consensus", END)

  return graph.compile()


def debate_state_to_artifacts(
  knowledge: KnowledgeBase,
  state: DebateState,
) -> DebateArtifacts:
  error = state.get("error")
  if error:
    raise DebateGraphError(error)

  return DebateArtifacts(
    knowledge=knowledge,
    context_report=state.get("context_report"),
    verification_report=state.get("verification_report"),
    risk_report=state.get("risk_report"),
    consensus_report=state.get("consensus_report"),
  )