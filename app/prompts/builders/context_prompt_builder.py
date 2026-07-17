import json

from app.ai.schemas.context_request import ContextRequest
from app.prompts.loader import PromptLoader
from app.prompts.prompt_name import PromptName

class ContextPromptBuilder:


    @staticmethod
    def build(
        request: ContextRequest,
    ) -> str:

        system_prompt = PromptLoader.load(
            PromptName.CONTEXT
        )

        knowledge_json = json.dumps(
            request.knowledge.model_dump(),
            indent=2,
            ensure_ascii=False,
        )

        return (
            f"{system_prompt}\n\n"
            "# KNOWLEDGE BASE\n\n"
            f"{knowledge_json}"
        )