from abc import ABC, abstractmethod

from app.ai.schemas.inference_request import InferenceRequest
from app.ai.schemas.inference_response import InferenceResponse


class InferenceClient(ABC):

    @abstractmethod
    def generate(
        self,
        request: InferenceRequest,
    ) -> InferenceResponse:
        raise NotImplementedError