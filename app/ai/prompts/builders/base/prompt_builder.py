from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from app.agents.domain.prompt import Prompt
TRequest = TypeVar("TRequest")


class PromptBuilder(ABC, Generic[TRequest]):
    """
    Base interface for all prompt builders.
    """

    @abstractmethod
    def build(
        self,
        request: TRequest,
    ) -> Prompt:
        """
        Returns:
            (
                system_prompt,
                user_prompt
            )
        """
        ...