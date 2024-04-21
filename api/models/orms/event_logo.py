from sqlalchemy import BigInteger, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4

from api.models.mixin import ekt_now
from api.models.orms.base import BaseORM
from api.models.mixin import DateORMMixin
from api.configuration.config import settings


class EventFileORM(BaseORM, DateORMMixin):
    event_logo_id = Column(BigInteger, primary_key=True)
    event_id = Column(ForeignKey('event.event_id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    s3_path = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False, server_default=ekt_now())

    event = relationship(
        'EventORM',
        back_populates='files',
        foreign_keys=[event_id],
        uselist=False,
        lazy='selectin'
    )

    @classmethod
    def create_s3_path(cls, name: str, generate_prefix: bool = True) -> str:
        return '/'.join(
            [settings.S3_EVENT_FILES_DIR, f'{uuid4().hex}_{name}' if generate_prefix else name]
        )

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.event_id} {self.genre}>'
