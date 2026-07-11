import json

from app.ai.registry import transcription_client

from app.ai.schemas.transcription_request import (
    TranscriptionRequest,
)

from app.schemas.video_artifacts import VideoArtifacts


class WhisperService:

    @staticmethod
    def process(
        artifacts: VideoArtifacts,
    ) -> VideoArtifacts:

        request = TranscriptionRequest(
            audio_path=artifacts.audio_path,
        )

        response = transcription_client.transcribe(request)

        transcript = response.transcript

        transcript_path = (
            artifacts.workspace.transcript_dir /
            "transcript.json"
        )

        with open(
            transcript_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                transcript.model_dump(),
                file,
                indent=4,
                ensure_ascii=False,
            )

        artifacts.transcript = transcript

        return artifacts