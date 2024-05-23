from sqlalchemy import BigInteger, Column, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from uuid import uuid4

from api.models.mixin import ekt_now
from api.models.orms.base import BaseORM
from api.models.mixin import DateORMMixin
from api.configuration.config import settings


class ExhibitFileORM(BaseORM, DateORMMixin):
    __table_args__ = (
        UniqueConstraint('exhibit_id'),
    )

    exhibit_logo_id = Column(BigInteger, primary_key=True)
    exhibit_id = Column(ForeignKey('exhibit.exhibit_id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    s3_path = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False, server_default=ekt_now())

    exhibit = relationship(
        'ExhibitORM',
        back_populates='image',
        foreign_keys=[exhibit_id],
        uselist=False,
        lazy='selectin'
    )

    @classmethod
    def create_s3_path(cls, name: str, generate_prefix: bool = True) -> str:
        return '/'.join(
            [settings.S3_EXHIBIT_FILES_DIR, f'{uuid4().hex}_{name}' if generate_prefix else name]
        )

    @property
    def can_delete(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.exhibit_id} {self.exhibit_logo_id} {self.s3_path}>'
