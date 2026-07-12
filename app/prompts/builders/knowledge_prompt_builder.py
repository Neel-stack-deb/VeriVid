from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.prompts.loader import PromptLoader


class KnowledgePromptBuilder:

    @staticmethod
    def build(request: KnowledgeRequest) -> str:

        prompt = PromptLoader.load("knowledge_prompt.md")

        return f"""
{prompt}

## Transcript

{request.transcript.model_dump_json(indent=2)}

## Scene Collection

{request.scenes.model_dump_json(indent=2)}
"""