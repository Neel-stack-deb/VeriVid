import subprocess

from app.exceptions.media import MediaProcessingError


class MediaExecutor:
    """
    Executes media processing commands (FFmpeg / FFprobe)
    and translates infrastructure errors into domain exceptions.
    """

    @staticmethod
    def run_ffmpeg(command: list[str]) -> None:
        MediaExecutor._run(command, "FFmpeg")

    @staticmethod
    def run_ffprobe(command: list[str]) -> str:
        return MediaExecutor._run(command, "FFprobe")

    @staticmethod
    def _run(command: list[str], tool_name: str) -> str:
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

            return result.stdout

        except FileNotFoundError as e:
            raise MediaProcessingError(
                f"{tool_name} is not installed or not available in PATH."
            ) from e

        except subprocess.CalledProcessError as e:
            raise MediaProcessingError(
                f"{tool_name} failed.\n{e.stderr}"
            ) from e