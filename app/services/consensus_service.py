from app.ai.analyzers.consensus_analyzer import ConsensusAnalyzer
from app.schemas.debate.debate_artifacts import DebateArtifacts


class ConsensusService:

    def __init__(
        self,
        analyzer: ConsensusAnalyzer,
    ):
        self._analyzer = analyzer

    def process(
        self,
        artifacts: DebateArtifacts,
    ) -> DebateArtifacts:

        artifacts.consensus_report = self._analyzer.analyze(
            artifacts
        )

        return artifacts