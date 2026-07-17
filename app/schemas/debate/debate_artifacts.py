from pydantic import BaseModel

from app.schemas.debate.consensus_report import ConsensusReport
from app.schemas.debate.context_report import ContextReport
from app.schemas.debate.risk_report import RiskReport
from app.schemas.debate.verification_report import VerificationReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class DebateArtifacts(BaseModel):
    knowledge: KnowledgeBase

    context_report: ContextReport | None = None

    verification_report: VerificationReport | None = None

    risk_report: RiskReport | None = None

    consensus_report: ConsensusReport | None = None