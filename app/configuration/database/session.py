from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Set

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.sql import ClauseElement

from app.utils.common import call_function
from app.utils.types import ListAny, Relationship


if TYPE_CHECKING:
    from app.models import BaseORM


class SessionListenerType(Enum):
    BEFORE_COMMIT = 'BEFORE_COMMIT'
    AFTER_COMMIT = 'AFTER_COMMIT'
    AFTER_REFRESH = 'AFTER_REFRESH'


class Session(AsyncSession):
    _changes: Dict[str, list]
    _listeners = defaultdict(list)

    async def commit(self) -> None:
        self._save_precommit_changes()
        for function in self._listeners[SessionListenerType.BEFORE_COMMIT]:
            await call_function(function, self)
        try:
            await super().commit()
        except SQLAlchemyError as err:
            if err:
                await super().rollback()
                raise
        for function in self._listeners[SessionListenerType.AFTER_COMMIT]:
            await call_function(function, self)

    async def fetch_all(self, query: ClauseElement | str, scalars: bool = True, unique: bool = True) -> ListAny:
        result = await self.execute(query)
        if unique:
            result = result.unique()
        if scalars:
            result = result.scalars()
        return result.all()

    async def fetch_one(self, query: ClauseElement | str) -> Any:
        return await self.scalar(query)

    def _save_precommit_changes(self) -> None:
        self._changes = {'added': list(self.new), 'updated': list(self.dirty), 'deleted': list(self.deleted)}

    @property
    def precommit_added(self) -> list:
        return self._changes['added']

    @property
    def precommit_updated(self) -> list:
        return self._changes['updated']

    @property
    def precommit_deleted(self) -> list:
        return self._changes['deleted']

    @classmethod
    def add_listener(cls, event: SessionListenerType, function: Callable[[Session], Any]) -> None:
        cls._listeners[event].append(function)

    async def _refresh(
        self,
        *objects: BaseORM,
        relationships: Dict[str, List[RelationshipProperty]],
        **kwargs: Any,
    ) -> None:
        for object_ in objects:
            await super().refresh(object_, **kwargs)
            relationships_copy = relationships.copy()
            for relationship in relationships_copy.pop(object_.__tablename__, []):
                relationship_object = getattr(object_, relationship.key)
                if relationship.uselist and len(relationship_object) > 0:
                    await self._refresh(*relationship_object, relationships=relationships_copy, **kwargs)
                elif not relationship.uselist and relationship_object is not None:
                    await self._refresh(relationship_object, relationships=relationships_copy, **kwargs)

    async def refresh(self, *objects: BaseORM, relationships: Iterable[Relationship] = None, **kwargs: Any) -> None:
        from ..models import AssociatedEntityORMMixin, SearchableORMMixin

        orms_affects_indexes = {
            type(obj) for obj in [*self.precommit_added, *self.precommit_updated, *self.precommit_deleted]
        }
        relationships: tuple[Relationship, ...] = tuple(relationships or [])
        indexes_orms = {type(obj) for obj in objects if isinstance(obj, SearchableORMMixin)}
        for orm_affects_indexes in orms_affects_indexes:
            for index_orm, relationship_paths in orm_affects_indexes.get_affected_indexes().items():
                indexes_orms.add(index_orm)
                relationships += (
                    relationship_paths
                    if isinstance(relationship_paths, tuple)
                    else tuple(tv for e in relationship_paths for tv in e)
                )
        for index_orm in indexes_orms:
            relationships += tuple(
                tv
                for searchable_relation in index_orm.__searchable_relations__
                for tv in index_orm.get_affected_indexes_path(index_orm, searchable_relation)
            )
        relationships: Set[RelationshipProperty] = {
            relationship if isinstance(relationship, RelationshipProperty) else relationship.property
            for relationship in relationships
        }
        relationships |= {
            type(object_).associated_entity.property
            for object_ in objects
            if isinstance(object_, AssociatedEntityORMMixin)
        }
        relationships_by_table_name = defaultdict(list)
        for relationship in relationships:
            relationships_by_table_name[relationship.parent.class_.__tablename__].append(relationship)
        await self._refresh(*objects, relationships=relationships_by_table_name, **kwargs)
        for function in self._listeners[SessionListenerType.AFTER_REFRESH]:
            await call_function(function, self)
