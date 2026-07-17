from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class BaseAnalyzer(
    ABC,
    Generic[Input, Output],
):

    @abstractmethod
    def analyze(
        self,
        data: Input,
    ) -> Output:
        """
        Analyze the input and return the corresponding report.
        """
        raise NotImplementedError