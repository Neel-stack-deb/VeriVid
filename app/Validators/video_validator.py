from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.constants import (
    ALLOWED_VIDEO_EXTENSIONS,
    ALLOWED_VIDEO_MIME_TYPES,
)


class VideoValidator:

    @staticmethod
    async def validate(file: UploadFile) -> None:

        VideoValidator.validate_extension(file)

        VideoValidator.validate_content_type(file)

    @staticmethod
    def validate_extension(file: UploadFile):

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_VIDEO_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file extension: {extension}",
            )

    @staticmethod
    def validate_content_type(file: UploadFile):

        if file.content_type not in ALLOWED_VIDEO_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported content type: {file.content_type}",
            )
