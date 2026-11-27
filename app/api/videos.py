import logging

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.repositories.video_workspace_repository import (
  VideoWorkspaceNotFoundError,
)
from app.schemas.api_errors import ErrorResponse
from app.schemas.api_videos import (
  DeleteVideoResponse,
  ProcessVideoResponse,
  VideoDetailResponse,
  VideoResultsResponse,
  VideoStatusResponse,
  VideoUploadResponse,
)
from app.services.video_api_service import VideoApiService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/videos", tags=["Videos"])
_service = VideoApiService()


@router.post(
  "/upload",
  response_model=VideoUploadResponse,
  status_code=status.HTTP_201_CREATED,
  responses={
    400: {"model": ErrorResponse},
    413: {"model": ErrorResponse},
  },
)
async def upload_video(video: UploadFile = File(...)) -> VideoUploadResponse:
  try:
    return await _service.upload_video(video)
  except HTTPException:
    raise
  except Exception as exc:
    logger.exception("Upload failed")
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Upload failed",
    ) from exc


@router.post(
  "/{video_id}/process",
  response_model=ProcessVideoResponse,
  responses={
    404: {"model": ErrorResponse},
  },
)
def process_video(video_id: str) -> ProcessVideoResponse:
  try:
    return _service.start_processing(video_id)
  except VideoWorkspaceNotFoundError as exc:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=str(exc),
    ) from exc


@router.get(
  "/{video_id}/status",
  response_model=VideoStatusResponse,
  responses={404: {"model": ErrorResponse}},
)
def video_status(video_id: str) -> VideoStatusResponse:
  try:
    return _service.get_status(video_id)
  except VideoWorkspaceNotFoundError as exc:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=str(exc),
    ) from exc


@router.get(
  "/{video_id}",
  response_model=VideoDetailResponse,
  responses={404: {"model": ErrorResponse}},
)
def video_detail(video_id: str) -> VideoDetailResponse:
  try:
    return _service.get_video_detail(video_id)
  except VideoWorkspaceNotFoundError as exc:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=str(exc),
    ) from exc


@router.get(
  "/{video_id}/results",
  response_model=VideoResultsResponse,
  responses={404: {"model": ErrorResponse}},
)
def video_results(video_id: str) -> VideoResultsResponse:
  try:
    return _service.get_results(video_id)
  except VideoWorkspaceNotFoundError as exc:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=str(exc),
    ) from exc


@router.delete(
  "/{video_id}",
  response_model=DeleteVideoResponse,
  responses={
    404: {"model": ErrorResponse},
    409: {"model": ErrorResponse},
  },
)
def delete_video(video_id: str) -> DeleteVideoResponse:
  try:
    return _service.delete_video(video_id)
  except VideoWorkspaceNotFoundError as exc:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=str(exc),
    ) from exc
  except RuntimeError as exc:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=str(exc),
    ) from exc