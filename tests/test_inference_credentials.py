import pytest

from app.ai.clients.fireworks_client import FireworksClient
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.inference_request import InferenceRequest
from app.exceptions.inference_exceptions import AuthenticationError


def test_fireworks_client_requires_credentials_on_generate():
  client = FireworksClient()
  request = InferenceRequest(
    model="test",
    system_prompt="system",
    user_prompt="user",
    response_model=ContextResponse,
  )

  with pytest.raises(AuthenticationError):
    client.generate(request)