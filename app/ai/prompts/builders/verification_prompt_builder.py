from app.ai.prompts.builders.base.prompt_builder import PromptBuilder
from app.ai.schemas.verification_request import VerificationRequest
from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.prompt_name import PromptName


class VerificationPromptBuilder(
    PromptBuilder[VerificationRequest]
):

    def build(
        self,
        request: VerificationRequest,
    ) -> tuple[str, str]:

        system_prompt = PromptLoader.load(
            PromptName.VERIFICATION
        )

        user_prompt = f"""
# KNOWLEDGE BASE

{request.knowledge.model_dump_json(indent=2)}

# CONTEXT ANALYSIS

{request.context.model_dump_json(indent=2)}
"""

        return system_prompt, user_prompt