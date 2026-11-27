from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.graph.debate_graph import build_debate_graph, debate_state_to_artifacts
from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.services.debate_persistence_service import DebatePersistenceService


class DebatePipeline:

  def __init__(
    self,
    context_agent: ContextAgent,
    verification_agent: VerificationAgent,
    risk_agent: RiskAgent,
    consensus_agent: ConsensusAgent,
    persistence_service: DebatePersistenceService,
  ):
    self._persistence = persistence_service
    self._graph = build_debate_graph(
      context_agent=context_agent,
      verification_agent=verification_agent,
      risk_agent=risk_agent,
      consensus_agent=consensus_agent,
    )

  def process(
    self,
    workspace,
    knowledge: KnowledgeBase,
  ) -> DebateArtifacts:

    final_state = self._graph.invoke({"knowledge": knowledge})
    artifacts = debate_state_to_artifacts(knowledge, final_state)

    self._persistence.save(
      workspace,
      artifacts,
    )

    return artifacts