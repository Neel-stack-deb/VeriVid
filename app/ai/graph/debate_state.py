from typing import NotRequired, TypedDict

from app.schemas.debate.consensus_report import ConsensusReport
from app.schemas.debate.context_report import ContextReport
from app.schemas.debate.risk_report import RiskReport
from app.schemas.debate.verification_report import VerificationReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class DebateState(TypedDict):
  """LangGraph state for the debate council workflow."""

  knowledge: KnowledgeBase

  context_report: NotRequired[ContextReport | None]
  verification_report: NotRequired[VerificationReport | None]
  risk_report: NotRequired[RiskReport | None]
  consensus_report: NotRequired[ConsensusReport | None]

  error: NotRequired[str | None]


class DebateStateUpdate(TypedDict, total=False):
  """Partial update returned by graph nodes."""

  context_report: ContextReport | None
  verification_report: VerificationReport | None
  risk_report: RiskReport | None
  consensus_report: ConsensusReport | None
  error: str | None