from pathlib import Path
import subprocess

from app.core.constants import FRAME_SAMPLE_INTERVAL
from app.exceptions.frame import FrameExtractionError
from app.schemas.video_artifacts import VideoArtifacts

class FrameService:

    @staticmethod
    def extract_frames(artifacts: VideoArtifacts) -> VideoArtifacts:
        video_path = artifacts.video_path
        output_directory = Path("data/frames") / video_path.stem
        output_directory.mkdir(parents=True, exist_ok=True)

        output_pattern = output_directory / "frame_%04d.jpg"

        command = [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            f"fps=1/{FRAME_SAMPLE_INTERVAL}",
            str(output_pattern),
            "-y",
        ]

        try:
            subprocess.run(
                command,
                check=True,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, # Capture error stream in memory buffer
            )
        except subprocess.CalledProcessError as error:
            # Now you have access to the exact message FFmpeg spit out!
            print(f"FFmpeg failed with code {error.returncode}.")
            print(f"Reason: {error.stderr}")
            raise FrameExtractionError(
                f"Failed to extract frames from {video_path.name}"
            ) from error

        artifacts.frame_paths = sorted(output_directory.glob("*.jpg"))
        return artifacts