from app.ai.analyzers.verification_analyzer import VerificationAnalyzer
from app.schemas.debate.debate_artifacts import DebateArtifacts


class VerificationService:

    def __init__(
        self,
        analyzer: VerificationAnalyzer,
    ):
        self._analyzer = analyzer

    def process(
        self,
        artifacts: DebateArtifacts,
    ) -> DebateArtifacts:

        artifacts.verification_report = self._analyzer.analyze(
            artifacts.knowledge
        )

        return artifacts