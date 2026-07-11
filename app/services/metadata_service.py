import json
import subprocess
from pathlib import Path

from app.schemas.video_metadata import VideoMetadata


class MetadataService:

    @staticmethod
    def extract(video_path: Path) -> VideoMetadata:

        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        metadata = json.loads(result.stdout)

        video_stream = next(
            (stream
            for stream in metadata["streams"]
            if stream["codec_type"] == "video"),
            None
        )

        if not video_stream:
            raise ValueError(f"No video stream found in the file: {video_path.name}")

        numerator, denominator = map(
            int,
            video_stream["r_frame_rate"].split("/")
        )

        fps = numerator / denominator

        return VideoMetadata(
            filename=video_path.name,
            duration=float(metadata["format"]["duration"]),
            size=int(metadata["format"]["size"]),
            width=video_stream["width"],
            height=video_stream["height"],
            fps=fps,
            codec=video_stream["codec_name"],
        )