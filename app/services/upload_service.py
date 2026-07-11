from fastapi import UploadFile

from app.schemas.upload import UploadResponse
from app.services.workspace_service import WorkspaceService
from app.Validators.video_validator import VideoValidator

class UploadService:

    @staticmethod
    async def upload(video: UploadFile) -> UploadResponse:
        await VideoValidator.validate(video)
        workspace, size = await WorkspaceService.create(video)

        return UploadResponse(
            filename=video.filename,
            content_type=video.content_type,
            file_size=size,
            storage_path=str(workspace.video_path)
        )