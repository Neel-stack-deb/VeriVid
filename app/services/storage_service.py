from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.exceptions.storage import StorageError
from app.core.constants import UPLOAD_CHUNK_SIZE, MAX_VIDEO_SIZE, STORAGE_DIR

class StorageService:
    
    @staticmethod
    async def save_file(file: UploadFile) -> tuple[Path, int]:
        """
        Validates(Size validation lives here to not repeating the file read twice) and saves an uploaded video file using chunked streaming.
        
        Raises:
            HTTPException: If the file type is invalid or exceeds the size limit.
        """

        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        file_extension = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid4()}{file_extension}"
        destination_path = STORAGE_DIR / unique_filename

        total_bytes_written = 0

        # Stream and Validate File Size simultaneously
        try:
            with open(destination_path, "wb") as buffer:
                # Use UPLOAD_CHUNK_SIZE constant for reading
                while chunk := await file.read(UPLOAD_CHUNK_SIZE):
                    total_bytes_written += len(chunk)
                    
                    # Proactively check if the file size has crossed the threshold
                    if total_bytes_written > MAX_VIDEO_SIZE:
                        raise StorageError(
                            f"File exceeds the maximum allowed size of {MAX_VIDEO_SIZE // (1024 * 1024)} MB."
                        )
                        
                    buffer.write(chunk)

                if total_bytes_written == 0:
                    raise StorageError("Uploaded file is empty.")
                     

        except StorageError:
            # Clean up cleanup: If validation failed mid-stream or any other exception, delete the partial file
            if destination_path.exists():
                destination_path.unlink()
            raise  # Re-raise the exception so FastAPI handles the error response

        except OSError as e:
            if destination_path.exists():
                destination_path.unlink()

            raise StorageError(
                "Failed to write uploaded file to storage."
            ) from e
            
        finally:
            # Always close the upload file descriptor to free resources
            await file.close()

        return destination_path, total_bytes_written