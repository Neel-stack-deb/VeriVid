import subprocess
from pathlib import Path

from app.schemas.video_artifacts import VideoArtifacts
from app.exceptions.audio import AudioExtractionError


class AudioService:

    @staticmethod
    def process(artifacts: VideoArtifacts) -> VideoArtifacts:
        """
        Extracts mono 16 kHz WAV audio from the uploaded video.
        """

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
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_audio),
        ]

        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

        except FileNotFoundError as e:
            raise AudioExtractionError(
                "FFmpeg is not installed or not found in PATH."
            ) from e

        except subprocess.CalledProcessError as e:
            raise AudioExtractionError(
                f"Failed to extract audio.\n{e.stderr}"
            ) from e

        artifacts.audio_path = output_audio

        return artifacts