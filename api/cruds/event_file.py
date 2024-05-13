from fastapi import UploadFile
from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.models import EventFileORM, EventORM
from api.utils.s3 import upload_file_on_s3, delete_file_from_s3
from api.configuration.database import Session


@with_model(EventFileORM)
class EventFile(Base):
    simple_columns_to_update = {
        EventFileORM.name,
        EventFileORM.description,
        EventFileORM.s3_path,
    }

    fields_to_update = (
        simple_columns_to_update

    )

    @classmethod
    async def upload_file_on_s3(cls, file: UploadFile, public: bool, generate_prefix: bool = True) -> str:
        s3_path = EventFileORM.create_s3_path(file.filename, generate_prefix)
        await upload_file_on_s3(s3_path, file, public)
        return s3_path

    @classmethod
    async def delete_file_from_s3(cls, s3_path: str) -> None:
        await delete_file_from_s3(s3_path)

    @classmethod
    async def get_by_event_id(cls, session: Session, event_id: int) -> EventORM | None:
        query = select(cls.model).filter_by(event_id=event_id)
        return await session.fetch_one(query)
