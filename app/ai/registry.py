from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:
  from app.ai.clients.amd_client import AMDClient
  from app.ai.clients.base.inference_client import InferenceClient
  from app.ai.clients.fireworks_client import FireworksClient
  from app.ai.clients.qwen_vision_client import QwenVisionClient
  from app.ai.clients.transcription_client import TranscriptionClient
  from app.ai.clients.whisper_transcription_client import WhisperTranscriptionClient

T = TypeVar("T")


class _LazyProxy:
  """Defer client construction until first use (avoids heavy imports and credential checks at startup)."""

  def __init__(self, factory: Callable[[], T]) -> None:
    self._factory = factory
    self._instance: T | None = None

  def _get(self) -> T:
    if self._instance is None:
      self._instance = self._factory()
    return self._instance

  def __getattr__(self, item: str):
    return getattr(self._get(), item)


def _build_transcription_client() -> WhisperTranscriptionClient:
  from app.ai.clients.whisper_transcription_client import (
    WhisperTranscriptionClient,
  )

  return WhisperTranscriptionClient()


def _build_vision_client() -> QwenVisionClient:
  from app.ai.clients.qwen_vision_client import QwenVisionClient

  return QwenVisionClient()


def _build_reasoning_client() -> FireworksClient:
  from app.ai.clients.fireworks_client import FireworksClient

  return FireworksClient()


def _build_amd_client() -> AMDClient:
  from app.ai.clients.amd_client import AMDClient

  return AMDClient()


transcription_client: TranscriptionClient = _LazyProxy(_build_transcription_client)  # type: ignore[assignment]
vision_client: QwenVisionClient = _LazyProxy(_build_vision_client)  # type: ignore[assignment]
reasoning_client: InferenceClient = _LazyProxy(_build_reasoning_client)  # type: ignore[assignment]
amd_client: InferenceClient = _LazyProxy(_build_amd_client)  # type: ignore[assignment]