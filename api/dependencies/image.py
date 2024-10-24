from fastapi import UploadFile
from api.exceptions.base import ImageUploadError

MIME_TYPES = {"image/jpeg", "image/png", "image/jpg"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024


async def get_image_with(file: UploadFile) -> UploadFile:
    if file.content_type not in MIME_TYPES:
        raise ImageUploadError("Invalid type of image")

    if file.size > MAX_IMAGE_SIZE:
        raise ImageUploadError("The image is too large")

    return file
