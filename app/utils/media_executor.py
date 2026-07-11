import subprocess

from app.exceptions.media import MediaProcessingError


class MediaExecutor:

    @staticmethod
    def run(command: list[str]) -> None:
        """
        Executes an FFmpeg/FFprobe command.

        Raises:
            MediaProcessingError
        """

        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        except FileNotFoundError as e:
            raise MediaProcessingError(
                "FFmpeg is not installed or not available in PATH."
            ) from e

        except subprocess.CalledProcessError as e:
            raise MediaProcessingError(
                f"Media processing failed.\n{e.stderr}"
            ) from e