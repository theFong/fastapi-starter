import uuid

import varname
from fastapi_starter import database
from fastapi_starter.pagination import PaginationParams
from typing import (
    Optional,
    cast,
)
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from pydantic import EmailStr
from .prefix_id import PrefixId
from . import utils
from .database import Base, ChangeSet, Filters, Page, BaseIO


class UserId(PrefixId):
    prefix = "user"


class UserCreateAttrs(BaseIO):
    name: str
    email: EmailStr


class UserUpdateAttrs(BaseIO):
    name: Optional[str]
    email: Optional[EmailStr]


class User(Base):
    __tablename__ = "Users"

    id: UserId = cast(UserId, Column(String(50), primary_key=True, unique=True))
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    create_date = Column(DateTime(True), nullable=False)
    update_date = Column(DateTime(True), nullable=False)
    secret = Column(String(50), nullable=False)

    @classmethod
    def create(cls, *, attrs: UserCreateAttrs):
        id = UserId.make()
        now = utils.get_utc_now()
        secret = str(uuid.uuid4())
        return cls(
            id=id,
            name=attrs.name,
            email=attrs.email,
            create_date=now,
            secret=secret,
            update_date=now,
        )

    @classmethod
    def update(cls, *, attrs: UserUpdateAttrs) -> ChangeSet:
        update = False
        change_set = {}
        if attrs.name != None:
            update = True
            change_set[varname.nameof(cls.name)] = attrs.name
        if attrs.email != None:
            update = True
            change_set[varname.nameof(cls.email)] = attrs.email
        if update:
            change_set[varname.nameof(cls.update_date)] = utils.get_utc_now()
        return change_set

    @classmethod
    def get_by_id(cls, *, id: UserId, db_session: database.Session):
        user = db_session.query(cls).get(id)
        return user

    @classmethod
    def get_many(
        cls,
        *,
        pagination_params: PaginationParams,
        filters: Filters,
        db_session: database.Session
    ) -> Page["User"]:
        q = db_session.query(cls).filter(*filters).order_by(cls.create_date, cls.id)
        page, prev_page, next_page = database.page_query_results(q, pagination_params)
        return Page(prev_key=prev_page, items=page, next_key=next_page)

    @classmethod
    def use_email_filter(cls, email: EmailStr = None) -> database.Filters:
        if email is None:
            return []
        return [cls.email == email]  # type: ignore
