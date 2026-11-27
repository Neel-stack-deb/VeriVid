from app.ai.agents.domain.prompt import Prompt
from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.prompt_name import PromptName
from app.ai.schemas.knowledge_request import KnowledgeRequest


class KnowledgePromptBuilder:

  @staticmethod
  def build(request: KnowledgeRequest) -> Prompt:
    system_prompt = PromptLoader.load(PromptName.KNOWLEDGE)

    user_prompt = f"""## Transcript

{request.transcript.model_dump_json(indent=2)}

## Scene Collection

{request.scenes.model_dump_json(indent=2)}
"""

    return Prompt(
      system=system_prompt,
      user=user_prompt,
    )