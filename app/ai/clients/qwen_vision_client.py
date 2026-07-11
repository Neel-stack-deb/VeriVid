from app.ai.clients.base.vllm_client import VLLMClient
from app.ai.clients.vision_client import VisionClient
from app.ai.schemas.frame_vision_result import FrameVisionResult
from app.ai.schemas.vision_request import VisionRequest


class QwenVisionClient(
    VLLMClient,
    VisionClient,
):

    def analyze(
        self,
        request: VisionRequest,
    ) -> FrameVisionResult:
        raise NotImplementedError