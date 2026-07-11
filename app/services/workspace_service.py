from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.constants import (
    VIDEOS_DIR,
    UPLOAD_CHUNK_SIZE,
    MAX_VIDEO_SIZE,
)

from app.exceptions.storage import StorageError
from app.schemas.video_workspace import VideoWorkspace


class WorkspaceService:

    @staticmethod
    async def create(file: UploadFile) -> tuple[VideoWorkspace, int]:
        """
        Creates a workspace for one uploaded video and stores the original file.

        Returns:
            (VideoWorkspace, total_bytes_written)
        """

        video_id = str(uuid4())

        workspace_root = VIDEOS_DIR / video_id

        metadata_dir = workspace_root / "metadata"
        frames_dir = workspace_root / "frames"
        audio_dir = workspace_root / "audio"
        transcript_dir = workspace_root / "transcripts"
        report_dir = workspace_root / "reports"
        scenes_dir = workspace_root / "scenes"

        file_extension = Path(file.filename).suffix.lower()

        video_path = workspace_root / f"original{file_extension}"

        total_bytes_written = 0

        try:

            for directory in [
                metadata_dir,
                frames_dir,
                audio_dir,
                transcript_dir,
                report_dir,
                scenes_dir,
            ]:
                directory.mkdir(parents=True, exist_ok=True)

            with open(video_path, "wb") as buffer:

                while chunk := await file.read(UPLOAD_CHUNK_SIZE):

                    total_bytes_written += len(chunk)

                    if total_bytes_written > MAX_VIDEO_SIZE:
                        raise StorageError(
                            f"File exceeds the maximum allowed size of {MAX_VIDEO_SIZE // (1024 * 1024)} MB."
                        )

                    buffer.write(chunk)

                if total_bytes_written == 0:
                    raise StorageError("Uploaded file is empty.")

        except StorageError:

            if workspace_root.exists():
                import shutil
                shutil.rmtree(workspace_root)

            raise

        except OSError as e:

            if workspace_root.exists():
                import shutil
                shutil.rmtree(workspace_root)

            raise StorageError(
                "Failed to save uploaded file."
            ) from e

        finally:
            await file.close()

        workspace = VideoWorkspace(
            video_id=video_id,
            root=workspace_root,
            video_path=video_path,
            frames_dir=frames_dir,
            metadata_dir=metadata_dir,
            audio_dir=audio_dir,
            transcript_dir=transcript_dir,
            report_dir=report_dir,
            scenes_dir=scenes_dir,
        )

        return workspace, total_bytes_written

    @staticmethod
    def delete(workspace: VideoWorkspace) -> None:

        import shutil

        if workspace.root.exists():
            shutil.rmtree(workspace.root)