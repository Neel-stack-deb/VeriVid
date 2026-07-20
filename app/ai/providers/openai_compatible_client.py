from abc import ABC
from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.ai.clients.base.inference_client import InferenceClient
from app.ai.schemas.inference_request import InferenceRequest

T = TypeVar("T", bound=BaseModel)


class OpenAICompatibleClient(InferenceClient, ABC):

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
    ) -> None:

        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def generate(
        self,
        request: InferenceRequest,
    ) -> T:

        completion = self._client.beta.chat.completions.parse(
            model=request.model,
            messages=self._build_messages(request),
            response_format=request.response_model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        parsed = completion.choices[0].message.parsed

        if parsed is None:
            raise RuntimeError("LLM returned an empty structured response.")

        return parsed

    @staticmethod
    def _build_messages(
        request: InferenceRequest,
    ) -> list[dict[str, str]]:

        return [
            {
                "role": "system",
                "content": request.system_prompt,
            },
            {
                "role": "user",
                "content": request.user_prompt,
            },
        ]