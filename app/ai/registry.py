from app.ai.clients.whisper_transcription_client import (
    WhisperTranscriptionClient,
)
from app.ai.clients.gemma_client import GemmaClient
from app.ai.clients.qwen_vision_client import QwenVisionClient

transcription_client = WhisperTranscriptionClient()
vision_client = QwenVisionClient()
llm_client = GemmaClient()