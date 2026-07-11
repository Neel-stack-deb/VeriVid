from abc import ABC, abstractmethod

from pydantic import BaseModel


class InferenceClient(ABC):

    @abstractmethod
    def generate(
        self,
        request: BaseModel,
    ):
        pass