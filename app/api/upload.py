from fastapi import APIRouter, UploadFile, File

from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post(
    "",
    response_model=UploadResponse
)
async def upload_video(
    video: UploadFile = File(...)
):
    return await UploadService.upload(video)
