import json
import base64
import typing


import pydantic
import pydantic.generics

from fastapi.encoders import jsonable_encoder


from pydantic import validators


class PaginationKeyOut(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
        yield validators.str_validator

    @classmethod
    def validate(cls, v):
        if isinstance(v, tuple):
            key_str = json.dumps(jsonable_encoder(v))
            key_bytes = key_str.encode("ascii")
            base64_bytes = base64.b64encode(key_bytes)
            base64_key = base64_bytes.decode("ascii")
            return base64_key
        return v


class PaginationKeyIn(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
        yield validators.tuple_validator

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            base64_bytes = v.encode("ascii")
            message_bytes = base64.b64decode(base64_bytes)
            key_str = message_bytes.decode("ascii")
            key = json.loads(key_str)
            return key
        return v


T = typing.TypeVar("T", bound=pydantic.BaseModel)


class PageResponse(pydantic.generics.GenericModel, typing.Generic[T]):
    prev_key: typing.Optional[PaginationKeyOut]
    items: typing.List[T]
    next_key: typing.Optional[PaginationKeyOut]


PaginationKey = typing.Tuple[typing.Sequence, bool]
PaginationParams = typing.Tuple[typing.Optional[PaginationKey], int]


def use_params(key: PaginationKeyIn = None, offset: int = 25):
    return (key, offset)
