from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.services.debate_persistence_service import DebatePersistenceService
from app.agents.context_agent import ContextAgent
from app.agents.consensus_agent import ConsensusAgent
from app.agents.risk_agent import RiskAgent
from app.agents.verification_agent import VerificationAgent


class DebatePipeline:

    def __init__(
        self,
        context_agent: ContextAgent,
        verification_agent: VerificationAgent,
        risk_agent: RiskAgent,
        consensus_agent: ConsensusAgent,
        persistence_service: DebatePersistenceService,
    ):
        self._context = context_agent
        self._verification = verification_agent
        self._risk = risk_agent
        self._consensus = consensus_agent
        self._persistence = persistence_service

    def process(
        self,
        workspace,
        knowledge: KnowledgeBase,
    ) -> DebateArtifacts:

        artifacts = DebateArtifacts(
            knowledge=knowledge,
        )

        artifacts = self._context.process(artifacts)
        artifacts = self._verification.process(artifacts)
        artifacts = self._risk.process(artifacts)
        artifacts = self._consensus.process(artifacts)

        self._persistence.save(
            workspace,
            artifacts,
        )

        return artifacts