from fastapi import UploadFile

from app.schemas.upload import UploadResponse
from app.services.storage_service import StorageService


class UploadService:

    @staticmethod
    async def upload(video: UploadFile) -> UploadResponse:

        path, size = await StorageService.save_file(video)

        return UploadResponse(
            filename=video.filename,
            content_type=video.content_type,
            file_size=size,
            storage_path=str(path)
        )