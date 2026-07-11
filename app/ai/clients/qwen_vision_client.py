from app.ai.clients.vision_client import VisionClient
from app.ai.schemas.vision_request import VisionRequest
from app.ai.schemas.vision_response import VisionResponse


class QwenVisionClient(VisionClient):

    def analyze(
        self,
        request: VisionRequest,
    ) -> VisionResponse:
        raise NotImplementedError(
            "Qwen Vision client not implemented yet."
        )