from abc import ABC

from app.ai.clients.base.inference_client import InferenceClient
from app.ai.clients.base.vllm_client import VLLMClient
from app.ai.schemas.inference_request import InferenceRequest
from app.ai.schemas.inference_response import InferenceResponse


class OpenAICompatibleClient(VLLMClient, InferenceClient, ABC):

	def generate(
		self,
		request: InferenceRequest,
	) -> InferenceResponse:
		raise NotImplementedError


class FireworksClient(OpenAICompatibleClient):
	pass


class AMDClient(OpenAICompatibleClient):
	pass
