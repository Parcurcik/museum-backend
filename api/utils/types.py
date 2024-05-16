from enum import Enum
from typing import Any, Dict, Iterable, List, Literal, Set, Tuple, Type

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList, UnaryExpression
from starlette.responses import Response

ListAny = List[Any]
TupleAny = Tuple[Any, ...]

Number = int | float
OptionalNumber = Number | None

ListInt = List[int]
SetInt = Set[int]

IterableStr = Iterable[str]
ListStr = List[str]
SetStr = Set[str]
TupleStr = Tuple[str, ...]
TupleStrStr = Tuple[str, str]
OptionalListStr = ListStr | None
OptionalSetStr = SetStr | None

DictStrStr = Dict[str, str]

DictStrAny = Dict[str, Any]
ListDictStrAny = List[DictStrAny]
OptionalDictStrAny = DictStrAny | None

PKType = int
ListPK = List[PKType]
TupleStrPK = Tuple[str, PKType]

IterableColumn = Iterable[Column]
ListColumn = List[Column]
SetColumn = Set[Column]
TupleColumn = Tuple[Column, ...]

ORMField = InstrumentedAttribute | Column | RelationshipProperty
SetORMField = Set[ORMField]
Relationship = InstrumentedAttribute | RelationshipProperty
SetRelationship = Set[Relationship]

ResponseType = Response | BaseModel

File = str | UploadFile

TestsInfo = DictStrAny
VersionTestsInfo = Dict[str, DictStrAny]

WhereClause = BinaryExpression | BooleanClauseList
IterableWhereClause = Iterable[WhereClause]
OrderByClause = Tuple[Column | UnaryExpression, ...]

SortType = Literal['asc', 'desc']
ElasticsearchSortQuery = List[str | Dict[str, SortType] | DictStrAny]

RangeFilterValue = int
RangeFilterValueType = Type[int]
RangeFilter = Dict[Literal['gte', 'gt', 'lte', 'lt'], RangeFilterValue] | None

GenericAlias = type(list[int])


class FileTypesForSearchDownloading(str, Enum):
    csv = 'csv'
    xlsx = 'xlsx'
