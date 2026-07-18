from app.ai.clients.whisper_transcription_client import (
    WhisperTranscriptionClient,
)
from app.ai.clients.qwen_vision_client import QwenVisionClient
from app.ai.providers.openai_compatible_clients import FireworksClient

transcription_client = WhisperTranscriptionClient()
vision_client = QwenVisionClient()
reasoning_client = FireworksClient()