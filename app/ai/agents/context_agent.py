from app.ai.agents.base.base_agent import BaseAgent
from app.ai.prompts.builders.context_prompt_builder import ContextPromptBuilder
from app.ai.schemas.context_request import ContextRequest
from app.ai.schemas.context_response import ContextResponse


class ContextAgent(
    BaseAgent[
        ContextRequest,
        ContextResponse,
    ]
):

    MODEL_KEY = "debate"

    RESPONSE_MODEL = ContextResponse

    PROMPT_BUILDER = ContextPromptBuilder