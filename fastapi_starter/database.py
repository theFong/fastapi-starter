import pydantic
import sqlalchemy
from fastapi_starter.pagination import PaginationKey, PaginationParams

import functools
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)
from pydantic.generics import GenericModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sqlalchemy.sql.elements
from sqlalchemy.ext.declarative import declarative_base
import sqlakeyset
from sqlalchemy_continuum import make_versioned

from fastapi_starter import config


@functools.lru_cache(1)
def get_engine():
    engine = create_engine(
        config.get_config().db_dsn.get_secret_value(),
        native_datetime=True,
        echo=config.get_config().debug,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )
    return engine


def use_session() -> Iterator[Session]:
    engine = get_engine()
    with Session(engine) as session:  # type: ignore
        yield session


make_versioned(user_cls=None)  # must call before any models inited


def setup_models():
    sqlalchemy.orm.configure_mappers()


Base = declarative_base()
metadata = Base.metadata

E = TypeVar("E", bound=Base)


class Page(GenericModel, Generic[E]):
    class Config:
        arbitrary_types_allowed = True

    prev_key: Optional[PaginationKey] = None
    next_key: Optional[PaginationKey] = None
    items: List[E]


def page_query_results(
    query: sqlalchemy.orm.Query, pagination_params: PaginationParams
):
    key, offset = pagination_params
    page = sqlakeyset.get_page(query, per_page=offset, page=key)
    assert page.paging is not None
    prev_key: Optional[PaginationKey] = cast(
        PaginationKey,
        page.paging.previous if page.paging.has_previous else None,
    )
    next_key: Optional[PaginationKey] = cast(
        PaginationKey, page.paging.next if page.paging.has_next else None
    )
    return list(page), prev_key, next_key


def paginate(
    paged_func: Callable[..., Page[E]],
    params: Dict[Any, Any],
) -> Iterable[E]:
    pagination_params = params.pop("pagination_params", None)

    default_offset = 50
    if pagination_params is None:
        pagination_params = (None, default_offset)

    resp = paged_func(pagination_params=pagination_params, **params)
    for it in resp.items:
        yield it

    while resp.next_key is not None:
        pagination_params = (resp.next_key, pagination_params[1])
        resp = paged_func(pagination_params=pagination_params, **params)
        for it in resp.items:
            yield it


class Filter(sqlalchemy.sql.elements.BinaryExpression):  # type: ignore
    ...


Filters = Iterable[Filter]


class BaseIO(pydantic.BaseModel):
    class Config:
        orm_mode = True


ChangeSet = Dict[Union[str, Tuple[str]], Any]
