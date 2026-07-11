import json

from openai import BadRequestError

from app.ai.clients.base.vllm_client import VLLMClient
from app.ai.clients.vision_client import VisionClient
from app.ai.schemas.frame_vision_result import FrameVisionResult
from app.ai.schemas.vision_request import VisionRequest
from app.core.ai_settings import ai_settings
from app.utils.image_encoder import ImageEncoder

class QwenVisionClient(
    VLLMClient,
    VisionClient,
):

    def analyze(
        self,
        request: VisionRequest,
    ) -> FrameVisionResult:

        response = self.client.chat.completions.create(
            model=ai_settings.vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": request.prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": ImageEncoder.encode(request.image_path),
                            },
                        },
                    ],
                }
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        try:
            return FrameVisionResult.model_validate(
                json.loads(content)
            )

        except Exception as e:
            raise BadRequestError(
                f"Invalid vision response: {content}"
            ) from e