from app.agents.base_agent import BaseAgent
from app.schemas.debate.debate_artifacts import DebateArtifacts


class ConsensusAgent(BaseAgent):

    def process(
        self,
        artifacts: DebateArtifacts,
    ) -> DebateArtifacts:
        raise NotImplementedError