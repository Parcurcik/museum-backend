from fastapi import UploadFile
from api.cruds.base import Base, with_model

from api.models import EventFileORM
from api.utils.s3 import upload_file_on_s3, delete_file_from_s3
from api.configuration.database import Session


@with_model(EventFileORM)
class EventFile(Base):

    @classmethod
    async def upload_file_on_s3(cls, file: UploadFile, public: bool, generate_prefix: bool = True) -> str:
        s3_path = EventFileORM.create_s3_path(file.filename, generate_prefix)
        await upload_file_on_s3(s3_path, file, public)
        return s3_path

    @classmethod
    async def delete_file_from_s3(cls, s3_path: str) -> None:
        await delete_file_from_s3(s3_path)
