from openai import OpenAI

from app.core.ai_settings import ai_settings
from app.exceptions.inference_exceptions import AuthenticationError


class VLLMClient:

  def __init__(self) -> None:
    self._base_url = ai_settings.base_url.strip()
    self._api_key = ai_settings.api_key.strip()
    self._timeout = ai_settings.timeout
    self._client: OpenAI | None = None

  def _ensure_client(self) -> OpenAI:
    if not self._base_url or not self._api_key:
      raise AuthenticationError(
        "Vision provider credentials are not configured. "
        "Set AI_BASE_URL and AI_API_KEY."
      )
    if self._client is None:
      self._client = OpenAI(
        base_url=self._base_url,
        api_key=self._api_key,
        timeout=self._timeout,
      )
    return self._client

  @property
  def client(self) -> OpenAI:
    return self._ensure_client()