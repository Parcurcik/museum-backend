from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from api.configuration.config import settings


def camel_case_to_snake_case(input_str: str) -> str:
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


class BaseORM(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.NAMING_CONVENTION,
    )

    @declared_attr.directive
    def __model_name__(cls) -> str:
        return cls.__name__[:-3]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__model_name__)}"
