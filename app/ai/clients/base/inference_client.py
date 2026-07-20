from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from app.ai.schemas.inference_request import InferenceRequest

T = TypeVar("T", bound=BaseModel)


class InferenceClient(ABC):

    @abstractmethod
    def generate(
        self,
        request: InferenceRequest,
    ) -> T:
        ...