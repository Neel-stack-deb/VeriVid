from abc import abstractmethod

from app.ai.analyzers.base_analyzer import BaseAnalyzer
from app.schemas.debate.consensus_report import ConsensusReport
from app.schemas.debate.debate_artifacts import DebateArtifacts


class ConsensusAnalyzer(
    BaseAnalyzer[
        DebateArtifacts,
        ConsensusReport,
    ]
):

    @abstractmethod
    def analyze(
        self,
        data: DebateArtifacts,
    ) -> ConsensusReport:
        ...