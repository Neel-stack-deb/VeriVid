import json

from app.ai.prompts.builders.base.prompt_builder import PromptBuilder
from app.ai.schemas.context_request import ContextRequest
from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.prompt_name import PromptName
from app.ai.agents.domain.prompt import Prompt

class ContextPromptBuilder(
    PromptBuilder[ContextRequest]
):

    def build(
        self,
        request: ContextRequest,
    ) -> tuple[str, str]:

        system_prompt = PromptLoader.load(
            PromptName.CONTEXT,
        )

        knowledge_json = json.dumps(
            request.knowledge.model_dump(),
            indent=2,
            ensure_ascii=False,
        )

        user_prompt = (
            "# KNOWLEDGE BASE\n\n"
            f"{knowledge_json}"
        )

        return Prompt(
            system=system_prompt,
            user=user_prompt,
        )
        