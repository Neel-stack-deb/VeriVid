from app.ai.prompts.builders.base.prompt_builder import PromptBuilder
from app.ai.schemas.risk_request import RiskRequest
from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.prompt_name import PromptName


class RiskPromptBuilder(
    PromptBuilder[RiskRequest]
):

    def build(
        self,
        request: RiskRequest,
    ) -> tuple[str, str]:

        system_prompt = PromptLoader.load(
            PromptName.RISK
        )

        user_prompt = f"""
# KNOWLEDGE BASE

{request.knowledge.model_dump_json(indent=2)}

# CONTEXT ANALYSIS

{request.context.model_dump_json(indent=2)}

# VERIFICATION RESULTS

{request.verification.model_dump_json(indent=2)}
"""

        return system_prompt, user_prompt