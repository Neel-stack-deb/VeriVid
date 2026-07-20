from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar("TRequest")


class PromptBuilder(ABC, Generic[TRequest]):
    """
    Base interface for all prompt builders.
    """

    @abstractmethod
    def build(
        self,
        request: TRequest,
    ) -> tuple[str, str]:
        """
        Returns:
            (
                system_prompt,
                user_prompt
            )
        """
        ...