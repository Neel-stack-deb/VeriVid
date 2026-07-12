from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.prompts.loader import PromptLoader
from app.prompts.prompt_name import PromptName

class KnowledgePromptBuilder:

    @staticmethod
    def build(request: KnowledgeRequest) -> str:

        prompt = PromptLoader.load(PromptName.KNOWLEDGE)

        return f"""
{prompt}

## Transcript

{request.transcript.model_dump_json(indent=2)}

## Scene Collection

{request.scenes.model_dump_json(indent=2)}
"""