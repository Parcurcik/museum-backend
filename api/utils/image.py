import os
import shutil
from datetime import datetime

from fastapi import UploadFile, HTTPException
from api.configuration.config import settings


def save_event_image(file: UploadFile) -> str:
    event_dir = os.path.join(settings.STATIC_DIR, "event")

    if not os.path.exists(event_dir):
        os.makedirs(event_dir)

    current_date = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    extension = file.filename.split('.')[-1]
    filename = f"{current_date}.{extension}"
    file_path = os.path.join(event_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/static/event/{filename}"
