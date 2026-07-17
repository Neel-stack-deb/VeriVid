from app.ai.analyzers.risk_analyzer import RiskAnalyzer
from app.schemas.debate.debate_artifacts import DebateArtifacts


class RiskService:

    def __init__(
        self,
        analyzer: RiskAnalyzer,
    ):
        self._analyzer = analyzer

    def process(
        self,
        artifacts: DebateArtifacts,
    ) -> DebateArtifacts:

        artifacts.risk_report = self._analyzer.analyze(
            artifacts.knowledge
        )

        return artifacts