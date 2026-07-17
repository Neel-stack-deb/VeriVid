from abc import abstractmethod

from app.ai.analyzers.base_analyzer import BaseAnalyzer
from app.schemas.debate.context_report import ContextReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class ContextAnalyzer(
    BaseAnalyzer[
        KnowledgeBase,
        ContextReport,
    ]
):

    @abstractmethod
    def analyze(
        self,
        data: KnowledgeBase,
    ) -> ContextReport:
        ...