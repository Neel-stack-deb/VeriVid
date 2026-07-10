from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status
from app.core.constants import UPLOAD_CHUNK_SIZE, MAX_VIDEO_SIZE, ALLOWED_VIDEO_TYPES

class StorageService:
    STORAGE_DIR = Path("data/uploads")
    
    @classmethod
    async def save_file(cls, file: UploadFile) -> tuple[Path, int]:
        """
        Validates and saves an uploaded video file using chunked streaming.
        
        Raises:
            HTTPException: If the file type is invalid or exceeds the size limit.
        """
        # Validate File Type (MIME Content-Type)
        if file.content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_VIDEO_TYPES)}"
            )

        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid4()}{file_extension}"
        destination_path = cls.STORAGE_DIR / unique_filename

        total_bytes_written = 0

        # Stream and Validate File Size simultaneously
        try:
            with open(destination_path, "wb") as file_buffer:
                # Use UPLOAD_CHUNK_SIZE constant for reading
                while chunk_data := await file.read(UPLOAD_CHUNK_SIZE):
                    total_bytes_written += len(chunk_data)
                    
                    # Proactively check if the file size has crossed the threshold
                    if total_bytes_written > MAX_VIDEO_SIZE:
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"File exceeds maximum allowed size of {MAX_VIDEO_SIZE / (1024 * 1024):.0f}MB."
                        )
                        
                    file_buffer.write(chunk_data)
                    
        except HTTPException:
            # Clean up cleanup: If validation failed mid-stream, delete the partial file
            if destination_path.exists():
                destination_path.unlink()
            raise  # Re-raise the exception so FastAPI handles the error response
            
        finally:
            # Always close the upload file descriptor to free resources
            await file.close()

        return destination_path, total_bytes_written