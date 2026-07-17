from abc import abstractmethod

from app.ai.analyzers.base_analyzer import BaseAnalyzer
from app.schemas.debate.risk_report import RiskReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class RiskAnalyzer(
    BaseAnalyzer[
        KnowledgeBase,
        RiskReport,
    ]
):

    @abstractmethod
    def analyze(
        self,
        data: KnowledgeBase,
    ) -> RiskReport:
        ...