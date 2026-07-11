from pathlib import Path
import subprocess

from app.core.constants import FRAME_SAMPLE_INTERVAL


class FrameService:

    @staticmethod
    def extract_frames(video_path: Path) -> list[Path]:

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

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return sorted(output_directory.glob("*.jpg"))