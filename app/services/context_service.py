from app.ai.analyzers.context_analyzer import ContextAnalyzer
from app.schemas.debate.debate_artifacts import DebateArtifacts


class ContextService:

    def __init__(
        self,
        analyzer: ContextAnalyzer,
    ):
        self._analyzer = analyzer

    def process(
        self,
        artifacts: DebateArtifacts,
    ) -> DebateArtifacts:

        artifacts.context_report = self._analyzer.analyze(
            artifacts.knowledge
        )

        return artifacts