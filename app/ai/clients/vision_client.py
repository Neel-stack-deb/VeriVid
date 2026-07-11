from abc import ABC, abstractmethod

from app.ai.schemas.vision_request import VisionRequest
from app.ai.schemas.frame_vision_result import FrameVisionResult


class VisionClient(ABC):

    @abstractmethod
    def analyze(
        self,
        request: VisionRequest,
    ) -> FrameVisionResult:
        pass