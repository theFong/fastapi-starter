import functools
from typing import Iterator
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from fastapi_starter import config


@functools.lru_cache(1)
def get_engine():
    engine = create_engine(config.get_config().db_dsn.get_secret_value())
    return engine


def use_session() -> Iterator[Session]:
    engine = get_engine()
    with Session(engine) as session:  # type: ignore
        yield session
