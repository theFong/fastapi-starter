import contextlib
from datetime import datetime, timezone
from fastapi import exceptions

import sqlalchemy


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


@contextlib.contextmanager
def handle_constraint_error():
    try:
        yield
    except sqlalchemy.exc.IntegrityError as ie:
        error = str(ie).split("\n")[0].split(")")[-1].strip()
        raise exceptions.HTTPException(400, error)
