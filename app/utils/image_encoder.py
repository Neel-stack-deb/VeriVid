import base64
from pathlib import Path


class ImageEncoder:

    @staticmethod
    def encode(image_path: Path) -> str:
        if not image_path.exists():
            raise FileNotFoundError(image_path)

        image_bytes = image_path.read_bytes()

        encoded = base64.b64encode(image_bytes).decode("utf-8")

        extension = image_path.suffix.lower().replace(".", "")

        if extension == "jpg":
            extension = "jpeg"

        return (
            f"data:image/{extension};base64,"
            f"{encoded}"
        )