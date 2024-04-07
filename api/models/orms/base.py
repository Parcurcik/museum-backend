from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple, Type

from sqlalchemy import DDL, CheckConstraint, Column, Index, Table, UniqueConstraint, event, inspect
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, declared_attr
from sqlalchemy.orm import Mapper, QueryContext, RelationshipProperty

from api.utils.types import (
    DictStrAny,
    OptionalSetStr,
    PKType,
    SetColumn,
    SetORMField,
    SetRelationship,
    SetStr,
    TupleAny,
    TupleColumn,
    TupleStr,
)


def camel_to_snake_case(name: str) -> str:
    name = re.sub(r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', name)
    return name.lower().lstrip('_')


class MetaORM(DeclarativeMeta):
    _table_uniqueness_columns_names: SetStr | None = None

    def __init__(cls, classname: str, bases: Tuple[Type[object], ...], dict_: DictStrAny, **kwargs: Any) -> None:
        super().__init__(classname, bases, dict_, **kwargs)
        cls.__abstract__ = not classname.endswith('ORM') or classname == 'BaseORM'
        if cls._table_uniqueness_columns_names is None and not cls.__abstract__:
            cls._table_uniqueness_columns_names = {cls.get_pk_name()}

    @property
    def table_uniqueness_columns_names(cls) -> SetStr:
        if cls._table_uniqueness_columns_names is None:
            return set()
        return cls._table_uniqueness_columns_names.copy()

    @table_uniqueness_columns_names.setter
    def table_uniqueness_columns_names(cls, value: SetColumn | Index) -> None:
        match value:
            case set():
                cls._table_uniqueness_columns_names = {column.key for column in value}
            case Index():
                cls._table_uniqueness_columns_names = {column.key for column in value.columns}


Base = declarative_base(metaclass=MetaORM)


class BaseORM(Base):
    __abstract__ = True
    __table__: Table
    crud = None

    _memorize_changes: bool
    _changed_fields_names: SetStr

    __affects_indexes__: Dict[str, Tuple[SetORMField, ...] | List[Tuple[SetORMField, ...]]] = {}

    @classmethod
    def __table_cls__(cls, *args: Any, **kwargs: Any) -> Table:
        table = Table(*args, **kwargs)
        table.orm_class = cls
        return table

    @declared_attr
    def __model_name__(cls) -> str:
        return cls.__name__[:-3]  # 3 is len('ORM')

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__model_name__)

    @declared_attr
    def __table_separated_name__(cls) -> str:
        return cls.__tablename__.replace('_', ' ')

    card_type = __tablename__

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:  # don't use super call because our __init__ method is better for creation by API
        relationships = inspect(type(self)).relationships
        columns = self.__table__.columns
        columns_names = columns.keys()
        for column, value in kwargs.items():
            if (column in columns_names and ((value is None and columns[column].nullable) or value is not None)) or (
                column in relationships
                and (
                    (isinstance(value, list) and all(isinstance(o, relationships[column].mapper.class_) for o in value))
                    or (not relationships[column].uselist and isinstance(value, relationships[column].mapper.class_))
                )
            ):
                setattr(self, column, value)
        self._memorize_changes = True
        self._changed_fields_names = set()

    def __repr__(self) -> str:
        return f'<{self.__tablename__} {self.get_pk_value()}>'

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if getattr(self, '_memorize_changes', False) and (
            name in self.__table__.columns.keys() or name in inspect(type(self)).relationships
        ):
            self._changed_fields_names.add(name)

    @property
    def can_delete(self) -> bool:
        return True

    @property
    def columns_names(self) -> TupleStr:
        return self.get_columns_names()

    @property
    def changed_fields_names(self) -> TupleStr:
        return tuple(self._changed_fields_names)

    @property
    def is_modified(self) -> bool:
        return len(self._changed_fields_names) > 0

    @classmethod
    def get_columns_names(cls) -> TupleStr:
        return tuple(cls.__table__.columns.keys())

    @classmethod
    def get_pk_column(cls) -> Column:
        return cls.__table__.primary_key.columns[0]

    @classmethod
    def get_pk_name(cls) -> str:
        return cls.get_pk_column().key

    def get_pk_value(self) -> PKType:
        return getattr(self, self.get_pk_name())

    def get_values(self, columns_names: TupleStr) -> TupleAny:
        return tuple(getattr(self, column_name) for column_name in columns_names)

    @classmethod
    def get_unique_columns(cls) -> List[TupleColumn]:
        unique_columns_from_constraints = [
            tuple(constraint.columns)
            for constraint in cls.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        ]
        unique_columns_from_indexes = [tuple(index.columns) for index in cls.__table__.indexes if index.unique]
        return unique_columns_from_constraints + unique_columns_from_indexes

    @classmethod
    def get_unique_columns_names(cls) -> List[TupleStr]:
        return [tuple(column.key for column in columns) for columns in cls.get_unique_columns()]

    @classmethod
    def get_checked_columns(cls) -> Dict[str, TupleColumn]:
        return {
            constraint.name: tuple(constraint.columns)
            for constraint in cls.__table__.constraints
            if isinstance(constraint, CheckConstraint)
        }

    @classmethod
    def get_checked_columns_names(cls) -> Dict[str, TupleStr]:
        return {name: tuple(column.key for column in columns) for name, columns in cls.get_checked_columns().items()}

    @classmethod
    def get_orm_by_table_name(cls, table_name: str) -> Type[BaseORM]:
        return cls.registry.metadata.tables[table_name].orm_class

    @classmethod
    def get_delete_from_data_origin_func(cls) -> DDL:
        return DDL(
            'CREATE OR REPLACE FUNCTION delete_from_data_origin() RETURNS TRIGGER AS $$ '
            'DECLARE '
            '_old_id bigint := (to_json(OLD)->>TG_ARGV[0])::bigint; '
            'BEGIN '
            'DELETE FROM data_origin WHERE table_name = TG_TABLE_NAME AND row_id = _old_id; '
            'RETURN NULL; '
            'END; $$ LANGUAGE plpgsql'
        )

    @classmethod
    def get_trigger_for_delete_from_data_origin_func(cls) -> DDL:
        return DDL(
            f'CREATE TRIGGER delete_{cls.__tablename__}_from_data_origin AFTER DELETE ON {cls.__tablename__} '
            f'FOR EACH ROW EXECUTE PROCEDURE delete_from_data_origin(\'{cls.get_pk_name()}\');'
        )

    def orm2dict(self, relation_level: bool = False) -> DictStrAny:
        data = {column_name: getattr(self, column_name) for column_name in self.columns_names}
        if relation_level:
            return data
        for relation_name, relationship in inspect(type(self)).relationships.items():
            if relationship.uselist:
                data[relation_name] = [
                    relation_object.orm2dict(True) for relation_object in getattr(self, relation_name)
                ]
            else:
                relation_object = getattr(self, relation_name)
                data[relation_name] = relation_object.orm2dict(True) if relation_object is not None else None
        return data

    @classmethod
    def get_affected_indexes_path(
        cls, start_type: Type[BaseORM], path: Tuple[SetORMField, ...]
    ) -> Tuple[SetRelationship, ...]:
        relationship_path = ()
        object_type = start_type
        for p in path:
            if isinstance(p, str):
                p = getattr(object_type, p)
            relationship_path += (p,)
            object_type = (p if isinstance(p, RelationshipProperty) else p.property).mapper.class_
        return relationship_path

    @classmethod
    def get_affected_indexes(
        cls,
    ) -> Dict[Type[BaseORM], Tuple[SetRelationship, ...] | List[Tuple[SetRelationship, ...]]]:
        return {
            cls.get_orm_by_table_name(key): cls.get_affected_indexes_path(cls, value)
            if isinstance(value, tuple)
            else [cls.get_affected_indexes_path(cls, v) for v in value]
            for key, value in cls.__affects_indexes__.items()
        }


@event.listens_for(Mapper, 'load')
def init_on_load(target: BaseORM, context: QueryContext) -> None:  # noqa U100
    target._memorize_changes = True
    target._changed_fields_names = set()


@event.listens_for(Mapper, 'refresh')
def init_on_refresh(target: BaseORM, context: QueryContext, attrs: OptionalSetStr) -> None:  # noqa U100
    target._memorize_changes = True
    target._changed_fields_names = set()
