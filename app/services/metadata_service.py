import json
import subprocess
from pathlib import Path

from app.schemas.video_metadata import VideoMetadata
from app.exceptions.metadata import MetadataExtractionError
from app.schemas.video_artifacts import VideoArtifacts

class MetadataService:

    @staticmethod
    def extract(artifacts: VideoArtifacts) -> VideoArtifacts:
        video_path = artifacts.video_path
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as e:
            raise MetadataExtractionError(
                f"Failed to extract metadata from {video_path.name}"
            ) from e

        metadata = json.loads(result.stdout)

        video_stream = next(
            (stream
            for stream in metadata["streams"]
            if stream["codec_type"] == "video"),
            None
        )

        if not video_stream:
            raise MetadataExtractionError(f"No video stream found in the file: {video_path.name}")

        numerator, denominator = map(
            int,
            video_stream["r_frame_rate"].split("/")
        )

        fps = numerator / denominator

        artifacts.metadata =  VideoMetadata(
            filename=video_path.name,
            duration=float(metadata["format"]["duration"]),
            size=int(metadata["format"]["size"]),
            width=video_stream["width"],
            height=video_stream["height"],
            fps=fps,
            codec=video_stream["codec_name"],
        )

        return artifacts