from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.services.debate_persistence_service import DebatePersistenceService
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.schemas.context_request import ContextRequest
from app.ai.schemas.verification_request import VerificationRequest
from app.ai.schemas.risk_request import RiskRequest
from app.ai.schemas.consensus_request import ConsensusRequest

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

        # Context
        context_response = self._context.process(
            ContextRequest(
                knowledge=knowledge,
            )
        )

        artifacts.context_report = context_response.report

        # Verification
        verification_response = self._verification.process(
            VerificationRequest(
                knowledge=knowledge,
                context=context_response.report,
            )
        )

        artifacts.verification_report = verification_response.report

        # Risk
        risk_response = self._risk.process(
            RiskRequest(
                knowledge=knowledge,
                context=context_response.report,
                verification=verification_response.report,
            )
        )

        artifacts.risk_report = risk_response.report

        # Consensus
        consensus_response = self._consensus.process(
            ConsensusRequest(
                knowledge=knowledge,
                context=context_response.report,
                verification=verification_response.report,
                risk=risk_response.report,
            )
        )

        artifacts.consensus_report = consensus_response.report

        self._persistence.save(
            workspace,
            artifacts,
        )

        return artifacts