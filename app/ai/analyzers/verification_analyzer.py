from abc import abstractmethod

from app.ai.analyzers.base_analyzer import BaseAnalyzer
from app.schemas.debate.verification_report import VerificationReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class VerificationAnalyzer(
    BaseAnalyzer[
        KnowledgeBase,
        VerificationReport,
    ]
):

    @abstractmethod
    def analyze(
        self,
        data: KnowledgeBase,
    ) -> VerificationReport:
        ...