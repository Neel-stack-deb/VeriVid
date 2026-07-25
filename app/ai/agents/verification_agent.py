from app.ai.agents.base.base_agent import BaseAgent
from app.schemas.debate.debate_artifacts import DebateArtifacts


class VerificationAgent(BaseAgent):

    def process(
        self,
        artifacts: DebateArtifacts,
    ) -> DebateArtifacts:
        raise NotImplementedError