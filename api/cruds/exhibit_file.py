from fastapi import UploadFile
from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.models import ExhibitFileORM, ExhibitORM
from api.utils.s3 import upload_file_on_s3, delete_file_from_s3
from api.configuration.database import Session


@with_model(ExhibitFileORM)
class ExhibitFile(Base):
    simple_columns_to_update = {
        ExhibitFileORM.name,
        ExhibitFileORM.description,
        ExhibitFileORM.s3_path,
    }

    fields_to_update = (
        simple_columns_to_update

    )

    @classmethod
    async def upload_file_on_s3(cls, file: UploadFile, public: bool, generate_prefix: bool = True) -> str:
        s3_path = ExhibitFileORM.create_s3_path(file.filename, generate_prefix)
        await upload_file_on_s3(s3_path, file, public)
        return s3_path

    @classmethod
    async def delete_file_from_s3(cls, s3_path: str) -> None:
        await delete_file_from_s3(s3_path)

    @classmethod
    async def get_by_exhibit_id(cls, session: Session, exhibit_id: int) -> ExhibitORM | None:
        query = select(cls.model).filter_by(exhibit_id=exhibit_id)
        return await session.fetch_one(query)
