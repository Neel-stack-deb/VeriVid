from app.ai.clients.amd_client import AMDClient
from app.ai.clients.fireworks_client import FireworksClient
from app.ai.clients.whisper_transcription_client import (
    WhisperTranscriptionClient,
)
from app.ai.clients.qwen_vision_client import QwenVisionClient

transcription_client = WhisperTranscriptionClient()

vision_client = QwenVisionClient()

reasoning_client = FireworksClient()

amd_client = AMDClient()