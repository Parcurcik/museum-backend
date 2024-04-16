from datetime import date, datetime
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql.psycopg2 import PGCompiler_psycopg2
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.functions import FunctionElement

from api.utils.common import now


class ekt_now(FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(ekt_now, 'postgresql')
def pg_ekb_now(element: ekt_now, compiler: PGCompiler_psycopg2, **kwargs: Any) -> str:
    return 'TIMEZONE(\'ASIA/YEKATERINBURG\', CURRENT_TIMESTAMP)'


class DateORMMixin:
    created_at = Column(DateTime, default=now, nullable=False, server_default=ekt_now())
    updated_at = Column(DateTime, default=now, onupdate=now, nullable=False, server_default=ekt_now())

    @classmethod
    def now(cls) -> datetime:
        return now()

    @classmethod
    def date_now(cls) -> date:
        return now().date()

    @classmethod
    def mos_now(cls) -> FunctionElement:
        return ekt_now()
