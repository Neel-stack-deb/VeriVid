from app.ai.agents.base.base_agent import BaseAgent
from app.ai.prompts.builders.risk_prompt_builder import RiskPromptBuilder
from app.ai.schemas.risk_request import RiskRequest
from app.ai.schemas.risk_response import RiskResponse


class RiskAgent(
    BaseAgent[
        RiskRequest,
        RiskResponse,
    ]
):

    MODEL_KEY = "debate"

    RESPONSE_MODEL = RiskResponse

    PROMPT_BUILDER = RiskPromptBuilder