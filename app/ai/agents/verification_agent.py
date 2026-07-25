from app.ai.agents.base.base_agent import BaseAgent
from app.ai.prompts.builders.verification_prompt_builder import (
    VerificationPromptBuilder,
)
from app.ai.schemas.verification_request import VerificationRequest
from app.ai.schemas.verification_response import VerificationResponse


class VerificationAgent(
    BaseAgent[
        VerificationRequest,
        VerificationResponse,
    ]
):

    MODEL_KEY = "debate"

    RESPONSE_MODEL = VerificationResponse

    PROMPT_BUILDER = VerificationPromptBuilder