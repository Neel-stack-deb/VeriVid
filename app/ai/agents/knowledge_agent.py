from app.ai.agents.base.base_agent import BaseAgent
from app.ai.clients.base.inference_client import InferenceClient
from app.ai.prompts.builders.knowledge_prompt_builder import (
  KnowledgePromptBuilder,
)
from app.ai.schemas.inference_request import InferenceRequest
from app.ai.schemas.knowledge_extraction_response import (
  KnowledgeExtractionResponse,
)
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.core.ai_settings import ai_settings


class KnowledgeAgent(BaseAgent):
  """
  Knowledge extraction uses a dedicated ``extract`` entrypoint and
  ``KnowledgePromptBuilder`` (static) rather than the generic ``process`` flow.
  """

  def __init__(
    self,
    reasoning_client: InferenceClient,
  ) -> None:
    self._client = reasoning_client

  def extract(
    self,
    request: KnowledgeRequest,
  ) -> KnowledgeExtractionResponse:

    prompt = KnowledgePromptBuilder.build(request)

    inference_request = InferenceRequest(
      model=ai_settings.models["debate"],
      system_prompt=prompt.system,
      user_prompt=prompt.user,
      response_model=KnowledgeExtractionResponse,
    )

    return self._client.generate(inference_request)