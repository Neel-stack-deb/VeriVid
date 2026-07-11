from pathlib import Path

from app.schemas.video_artifacts import VideoArtifacts
from app.utils.media_executor import MediaExecutor


class AudioService:

    @staticmethod
    def process(artifacts: VideoArtifacts) -> VideoArtifacts:

        video_path = artifacts.workspace.video_path

        output_audio = (
            artifacts.workspace.audio_dir /
            "audio.wav"
        )

        command = [
            "ffmpeg",

            "-y",

            "-i",
            str(video_path),

            "-vn",

            "-acodec",
            "pcm_s16le",

            "-ar",
            "16000",

            "-ac",
            "1",

            str(output_audio),
        ]

        MediaExecutor.run(command)

        artifacts.audio_path = output_audio

        return artifacts