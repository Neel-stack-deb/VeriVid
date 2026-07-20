import logging
from abc import ABC, abstractmethod
from typing import TypeVar

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError as OpenAIAuthenticationError,
    OpenAI,
)
from pydantic import BaseModel

from app.ai.clients.base.inference_client import InferenceClient
from app.ai.schemas.inference_request import InferenceRequest
from app.exceptions.inference_exceptions import (
    AuthenticationError,
    InferenceError,
    ProviderConnectionError,
    ProviderTimeoutError,
    StructuredOutputError,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class OpenAICompatibleClient(
    InferenceClient,
    ABC,
):

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
    ):

        self._client = self._create_client(
            base_url,
            api_key,
        )

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------

    def generate(
        self,
        request: InferenceRequest,
    ) -> T:

        self._validate_request(request)

        self._log_request(request)

        try:

            completion = self._client.beta.chat.completions.parse(
                model=request.model,
                messages=self._build_messages(request),
                response_format=request.response_model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            response = self._parse_response(completion)

            self._log_response(request)

            return response

        except Exception as exc:

            self._handle_exception(exc)

    # ----------------------------------------------------
    # Client
    # ----------------------------------------------------

    @staticmethod
    def _create_client(
        base_url: str,
        api_key: str,
    ) -> OpenAI:

        return OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    # ----------------------------------------------------
    # Helpers
    # ----------------------------------------------------

    @staticmethod
    def _build_messages(
        request: InferenceRequest,
    ) -> list[dict]:

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

    @staticmethod
    def _validate_request(
        request: InferenceRequest,
    ):

        if not request.model:
            raise ValueError("Model cannot be empty.")

        if not request.system_prompt:
            raise ValueError("System prompt cannot be empty.")

        if not request.user_prompt:
            raise ValueError("User prompt cannot be empty.")

        if request.max_tokens <= 0:
            raise ValueError("max_tokens must be positive.")

    @staticmethod
    def _parse_response(
        completion,
    ) -> T:

        parsed = completion.choices[0].message.parsed

        if parsed is None:
            raise StructuredOutputError(
                "Provider returned invalid structured output."
            )

        return parsed

    @staticmethod
    def _handle_exception(
        exc: Exception,
    ):

        if isinstance(exc, OpenAIAuthenticationError):
            raise AuthenticationError from exc

        if isinstance(exc, APIConnectionError):
            raise ProviderConnectionError from exc

        if isinstance(exc, APITimeoutError):
            raise ProviderTimeoutError from exc

        if isinstance(exc, InferenceError):
            raise exc

        raise InferenceError(str(exc)) from exc

    # ----------------------------------------------------
    # Logging
    # ----------------------------------------------------

    def _log_request(
        self,
        request: InferenceRequest,
    ):

        logger.info(
            "[%s] Request | model=%s",
            self._provider_name(),
            request.model,
        )

    def _log_response(
        self,
        request: InferenceRequest,
    ):

        logger.info(
            "[%s] Response | model=%s",
            self._provider_name(),
            request.model,
        )

    # ----------------------------------------------------
    # Provider
    # ----------------------------------------------------

    @abstractmethod
    def _provider_name(self) -> str:
        ...