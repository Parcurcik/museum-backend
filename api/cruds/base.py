from typing import Callable, TypeVar, Type, Any, Dict, List, Tuple, Set
from sqlalchemy import select, insert, inspect
from sqlalchemy.orm import RelationshipProperty

from api.utils.common import all_in, get_difference, get_values_from_dict
from api.utils.types import TupleStr, PKType, DictStrAny, IterableColumn, SetRelationship, SetColumn, ORMField
from api.models import BaseORM
from api.configuration.database import Session

from api.exceptions import (
    CheckViolationError,
    DeletionError,
    ForeignKeyViolationError,
    ModelNotFoundError,
    NotNullViolationError,
    PSQLCheckViolationError,
    PSQLForeignKeyViolationError,
    PSQLIntegrityError,
    PSQLNotNullViolationError,
    PSQLUniqueViolationError,
    UniqueViolationError,
    get_info_from_check_violation_error,
    get_info_from_foreign_key_violation_error,
    get_info_from_not_null_violation_error,
    get_info_from_unique_violation_error,
    IncorrectRelationObjectError
)


class Base:
    model = BaseORM

    relations_to_create_before_creation: SetRelationship = set()
    relations_to_create_after_creation: SetRelationship = set()

    simple_columns_to_update: SetColumn = set()
    relations_to_update: SetRelationship = set()
    fields_to_update: Set[ORMField | str] = set()

    imaginary_check_constraints_columns: Dict[str, TupleStr] = {}

    @classmethod
    def create_object(cls, data: DictStrAny) -> model:
        return cls.model(**data)

    @classmethod
    async def get_by_id(cls, session: Session, id_: PKType) -> model | None:
        query = select(cls.model).where(cls.model.get_pk_column() == id_)
        return await session.fetch_one(query)

    @classmethod
    async def check_existence(cls, session: Session, id_: PKType) -> model:
        object_ = await cls.get_by_id(session, id_)
        if object_ is None:
            raise ModelNotFoundError(cls.model.__tablename__, (cls.model.get_pk_name(),), (str(id_),))
        return object_

    @classmethod
    def check_not_nullable_creation(cls, error: PSQLIntegrityError) -> None:
        if not isinstance(error, PSQLNotNullViolationError):
            return
        field = get_info_from_not_null_violation_error(error)
        if field in cls.model.get_columns_names():
            raise NotNullViolationError(error, field)

    @classmethod
    def check_unique_creation(cls, error: PSQLIntegrityError) -> None:
        if not isinstance(error, PSQLUniqueViolationError):
            return
        fields, values = get_info_from_unique_violation_error(error)
        for unique_columns_names in cls.model.get_unique_columns_names():
            if fields == unique_columns_names:
                raise UniqueViolationError(error, fields, values)

    @classmethod
    def check_foreign_creation(cls, error: PSQLIntegrityError) -> None:
        if not isinstance(error, PSQLForeignKeyViolationError):
            return
        fields, values, foreign_table_name = get_info_from_foreign_key_violation_error(error)
        for foreign_key in cls.model.__table__.foreign_keys:
            if fields == tuple(foreign_key.constraint.column_keys):
                raise ForeignKeyViolationError(error, fields, values, foreign_table_name)

    @classmethod
    def check_checked_creation(cls, error: PSQLIntegrityError) -> None:
        if not isinstance(error, PSQLCheckViolationError):
            return
        constraint = get_info_from_check_violation_error(error)
        real_columns_names = cls.model.get_checked_columns_names().get(constraint, None)
        imaginary_columns_names = cls.imaginary_check_constraints_columns.get(constraint, None)
        columns_names = real_columns_names or imaginary_columns_names
        if columns_names is not None:
            raise CheckViolationError(error, columns_names, constraint)

    @classmethod
    def _prepare_new_relation(
            cls,
            new_relation: DictStrAny,
            relation_relations: Dict[str, RelationshipProperty],
    ) -> None:
        for relation_name, relation_prop in relation_relations.items():
            if relation_name not in new_relation:
                continue
            for pair in relation_prop.local_remote_pairs:
                remote_value = (
                    new_relation[relation_name].get(pair[1].key)
                    if isinstance(new_relation[relation_name], dict)
                    else getattr(new_relation[relation_name], pair[1].key, None)
                )
                if remote_value is None:
                    break
                new_relation[pair[0].key] = remote_value

    @classmethod
    def _get_new_relations_dict(
            cls, relations_list: List[Any], relationship: RelationshipProperty, unique_columns_names: TupleStr
    ) -> Dict[TupleStr, DictStrAny]:
        try:
            relation_relations = inspect(relationship.mapper.class_).relationships
            new_relations_dict = {}
            for new_relation in relations_list:
                cls._prepare_new_relation(new_relation, relation_relations)
                new_relation['__all_unique__'] = all_in(unique_columns_names, new_relation)
                if new_relation['__all_unique__']:
                    new_relations_dict[get_values_from_dict(new_relation, unique_columns_names)] = new_relation
        except TypeError as exc:
            raise IncorrectRelationObjectError(
                cls.model.__tablename__, relationship.key, [dict], exc.args[0].split(' ', 1)[0][1:-1]
            )
        except KeyError:
            raise IncorrectRelationObjectError(cls.model.__tablename__, relationship.key, [dict], type(None))
        return new_relations_dict

    @classmethod
    async def _update_relation_in_list_on_update(
            cls,
            session: Session,
            new_relation_object: Any,
            old_relation_object: BaseORM,
            relationship: RelationshipProperty,
            **update_kwargs: Any,
    ) -> BaseORM:
        if isinstance(new_relation_object, dict):
            return await relationship.mapper.class_.crud.update_object(
                session,
                new_relation_object,
                old_relation_object,
                **update_kwargs,
            )
        else:
            raise IncorrectRelationObjectError(
                cls.model.__tablename__, relationship.key, [dict], type(new_relation_object)
            )

    @classmethod
    async def _update_relations_list_on_update(
            cls,
            session: Session,
            relations_list: List[Any],
            object_: model,
            relationship: RelationshipProperty,
            **update_kwargs: Any,
    ) -> Tuple[List[BaseORM], bool]:
        foreign_key_name = relationship.local_remote_pairs[0][1].key
        pk_value = object_.get_pk_value()
        unique_columns_names = tuple(
            column_name
            for column_name in relationship.mapper.class_.table_uniqueness_columns_names
            if column_name != foreign_key_name
        )
        old_relations_list = getattr(object_, relationship.key)
        old_relations_ids = (old_relation.get_values(unique_columns_names) for old_relation in old_relations_list)
        new_relations_dict = cls._get_new_relations_dict(relations_list, relationship, unique_columns_names)
        to_add, to_update, to_delete = get_difference(old_relations_ids, new_relations_dict.keys())
        need_update = len(to_add) > 0 or len(to_delete) > 0
        new_relations_list = []
        for old_relation in old_relations_list:
            ids = old_relation.get_values(unique_columns_names)
            if ids in to_update:
                new_relations_list.append(
                    await cls._update_relation_in_list_on_update(
                        session,
                        new_relations_dict[ids],
                        old_relation,
                        relationship,
                        **update_kwargs,
                    )
                )
                need_update |= old_relation.is_modified
            elif ids in to_delete:
                await relationship.mapper.class_.crud.delete_object(session, old_relation)
        for new_relation in relations_list:
            ids = None
            if (
                    not new_relation['__all_unique__']
                    or (ids := get_values_from_dict(new_relation, unique_columns_names)) in to_add
            ):
                new_relation.update({foreign_key_name: pk_value})
                new_relations_list.append(await relationship.mapper.class_.crud.create(session, new_relation))
                if ids is not None:
                    to_add.remove(ids)
        return new_relations_list, need_update

    @classmethod
    async def _update_relation_on_update(
            cls,
            session: Session,
            relation_object: Any,
            object_: model,
            relationship: RelationshipProperty,
            **update_kwargs: Any,
    ) -> Tuple[BaseORM, bool]:
        if isinstance(relation_object, dict):
            old_relation_object = getattr(object_, relationship.key)
            if old_relation_object is None:
                relation_object.update({relationship.back_populates: object_})
                return await relationship.mapper.class_.crud.create(session, relation_object), True
            else:
                old_relation_object = await relationship.mapper.class_.crud.update_object(
                    session,
                    relation_object,
                    old_relation_object,
                    **update_kwargs,
                )
                return old_relation_object, old_relation_object.is_modified
        else:
            raise IncorrectRelationObjectError(cls.model.__tablename__, relationship.key, [dict], type(relation_object))

    @classmethod
    async def _update_relations_on_update(
            cls,
            session: Session,
            object_: model,
            data: DictStrAny,
            **update_kwargs: Any,
    ) -> None:
        for relationship in cls.relations_to_update:
            if relationship.key not in data:
                continue
            relationship: RelationshipProperty = relationship.property
            if relationship.uselist:
                new_relation, need_update = await cls._update_relations_list_on_update(
                    session,
                    data[relationship.key],
                    object_,
                    relationship,
                    **update_kwargs,
                )
            else:
                new_relation, need_update = await cls._update_relation_on_update(
                    session,
                    data[relationship.key],
                    object_,
                    relationship,
                    **update_kwargs,
                )
            if need_update:
                setattr(object_, relationship.key, new_relation)

    @classmethod
    async def _update_complicated_fields(
            cls, session: Session, object_: model, data: DictStrAny, **update_kwargs: Any
    ) -> None:
        pass

    @classmethod
    async def _before_update(
            cls, session: Session, object_: model, data: DictStrAny, **update_kwargs: Any
    ) -> None:
        pass

    @classmethod
    def _need_to_update(cls, data: DictStrAny, object_: model) -> bool:
        fields = {field if isinstance(field, str) else field.key for field in cls.fields_to_update}
        simple_columns_to_update = {column.key for column in cls.simple_columns_to_update}
        return any(
            field in data and (field not in simple_columns_to_update or data[field] != getattr(object_, field))
            for field in fields
        )

    @classmethod
    async def _after_update(
            cls, session: Session, object_: model, data: DictStrAny, **update_kwargs: Any
    ) -> None:
        pass

    @classmethod
    def _update_simple_columns(cls, object_: model, data: DictStrAny, columns: IterableColumn) -> None:
        for column in columns:
            if (
                    column.key in data
                    and data[column.key] != getattr(object_, column.key)
                    and ((data[column.key] is None and column.nullable) or data[column.key] is not None)
            ):
                setattr(object_, column.key, data[column.key])

    @classmethod
    async def update_object(
            cls,
            session: Session,
            data: DictStrAny,
            object_: model,
            **update_kwargs: Any,
    ) -> model:
        await cls._before_update(session, object_, data, **update_kwargs)
        if not cls._need_to_update(data, object_):
            return object_
        cls._update_simple_columns(object_, data, cls.simple_columns_to_update)
        await cls._update_relations_on_update(session, object_, data, **update_kwargs)
        await cls._update_complicated_fields(session, object_, data, **update_kwargs)
        if object_.is_modified:
            session.add(object_)
            await cls._after_update(session, object_, data, **update_kwargs)
        return object_

    @classmethod
    async def update(
            cls,
            session: Session,
            data: DictStrAny,
            id_: PKType,
            **update_kwargs: Any,
    ) -> model:
        object_ = await cls.check_existence(session, id_)
        return await cls.update_object(session, data, object_, **update_kwargs)

    check_not_nullable_update = check_not_nullable_creation
    check_unique_update = check_unique_creation
    check_foreign_update = check_foreign_creation
    check_checked_update = check_checked_creation

    @classmethod
    async def create_and_save(cls, session: Session, data: DictStrAny) -> model:
        object_ = cls.create_object(data)
        stmt = insert(cls.model)
        pk_name = cls.model.get_pk_name()
        pk_value = (await session.execute(stmt, [object_.__dict__])).inserted_primary_key[0]
        try:
            await session.commit()
        except Exception as err:
            raise err
        setattr(object_, pk_name, pk_value)
        return object_

    @classmethod
    async def _before_delete(cls, object_: model) -> None:
        pass

    @classmethod
    async def delete_object(cls, session: Session, object_: model) -> model:
        if object_.can_delete:
            await cls._before_delete(object_)
            await session.delete(object_)
        else:
            raise DeletionError(cls.model.__tablename__, object_.get_pk_value())
        return object_

    @classmethod
    async def delete(cls, session: Session, id_: PKType) -> model:
        object_ = await cls.check_existence(session, id_)
        return await cls.delete_object(session, object_)


_BaseCRUDT = TypeVar('_BaseCRUDT', bound=Base)


def with_model(model: Type[BaseORM]) -> Callable:
    def dec(crud: _BaseCRUDT) -> _BaseCRUDT:
        crud.model = model
        model.crud = crud
        return crud

    return dec
