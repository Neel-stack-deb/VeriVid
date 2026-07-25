from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel

from app.ai.clients.base.inference_client import InferenceClient
from app.ai.prompts.builders.base.prompt_builder import PromptBuilder
from app.agents.domain.ai_model import AIModel
from app.ai.schemas.inference_request import InferenceRequest
from app.agents.domain.prompt import Prompt
from app.core.config import ai_settings

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse", bound=BaseModel)


class BaseAgent(
    ABC,
    Generic[TRequest, TResponse],
):
    """
    Base class for all AI reasoning agents.
    """

    MODEL_KEY: AIModel
    RESPONSE_MODEL: type[TResponse]
    PROMPT_BUILDER: type[PromptBuilder]

    def __init__(
        self,
        client: InferenceClient,
    ):
        self._client = client
        self._prompt_builder = self.PROMPT_BUILDER()

    def process(
        self,
        request: TRequest,
    ) -> TResponse:

        prompt = self._build_prompt(
            request,
        )

        inference_request = self._build_inference_request(
            prompt,
        )

        return self._execute(
            inference_request,
        )

    def _build_prompt(
        self,
        request: TRequest,
    ) -> Prompt:

        return self._prompt_builder.build(
            request,
        )

    def _build_inference_request(
        self,
        prompt: Prompt,
    ) -> InferenceRequest:

        return InferenceRequest(
            model=ai_settings.models[self.MODEL_KEY.value],
            system_prompt=prompt.system,
            user_prompt=prompt.user,
            response_model=self.RESPONSE_MODEL,
        )

    def _execute(
        self,
        request: InferenceRequest,
    ) -> TResponse:

        return self._client.generate(
            request,
        )