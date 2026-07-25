from app.ai.agents.base.base_agent import BaseAgent
from app.ai.prompts.builders.consensus_prompt_builder import (
    ConsensusPromptBuilder,
)
from app.ai.schemas.consensus_request import ConsensusRequest
from app.ai.schemas.consensus_response import ConsensusResponse


class ConsensusAgent(
    BaseAgent[
        ConsensusRequest,
        ConsensusResponse,
    ]
):

    MODEL_KEY = "debate"

    RESPONSE_MODEL = ConsensusResponse

    PROMPT_BUILDER = ConsensusPromptBuilder