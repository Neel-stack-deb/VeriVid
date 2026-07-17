from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.services.consensus_service import ConsensusService
from app.services.context_service import ContextService
from app.services.debate_persistence_service import DebatePersistenceService
from app.services.risk_service import RiskService
from app.services.verification_service import VerificationService


class DebatePipeline:

    def __init__(
        self,
        context_service: ContextService,
        verification_service: VerificationService,
        risk_service: RiskService,
        consensus_service: ConsensusService,
        persistence_service: DebatePersistenceService,
    ):
        self._context = context_service
        self._verification = verification_service
        self._risk = risk_service
        self._consensus = consensus_service
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