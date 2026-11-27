from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from app.ai.clients.base.inference_client import InferenceClient
from app.ai.clients.transcription_client import TranscriptionClient
from app.ai.clients.vision_client import VisionClient
from app.ai.schemas.inference_request import InferenceRequest
from app.ai.schemas.transcription_request import TranscriptionRequest
from app.ai.schemas.transcription_response import TranscriptionResponse
from app.ai.schemas.vision_request import VisionRequest
from app.ai.schemas.frame_vision_result import FrameVisionResult

T = TypeVar("T", bound=BaseModel)


class MockInferenceClient(InferenceClient):
  """Returns pre-configured Pydantic models keyed by response_model type."""

  def __init__(self, responses: dict[type[BaseModel], BaseModel] | None = None) -> None:
    self.responses = responses or {}
    self.calls: list[InferenceRequest] = []

  def register(self, model_type: type[BaseModel], value: BaseModel) -> None:
    self.responses[model_type] = value

  def generate(self, request: InferenceRequest) -> T:
    self.calls.append(request)
    response = self.responses.get(request.response_model)
    if response is None:
      raise RuntimeError(
        f"No mock registered for response model {request.response_model!r}"
      )
    return response  # type: ignore[return-value]


class MockVisionClient(VisionClient):

  def __init__(self, result: FrameVisionResult | None = None) -> None:
    self.result = result or FrameVisionResult(
      description="A test scene",
      objects=["object"],
      visible_text=["HELLO"],
    )
    self.calls: list[VisionRequest] = []

  def analyze(self, request: VisionRequest) -> FrameVisionResult:
    self.calls.append(request)
    return self.result


class MockTranscriptionClient(TranscriptionClient):

  def __init__(self, response: TranscriptionResponse) -> None:
    self.response = response
    self.calls: list[TranscriptionRequest] = []

  def transcribe(self, request: TranscriptionRequest) -> TranscriptionResponse:
    self.calls.append(request)
    return self.response