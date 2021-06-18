import uuid
from sqlalchemy.sql.elements import ColumnElement

import varname
from fastapi_starter import database
from fastapi_starter.pagination import PaginationParams
from typing import (
    Generic,
    Optional,
    TypeVar,
    cast,
)
from sqlalchemy import Column, DateTime, ForeignKey, String, util
from sqlalchemy.orm import relationship

from pydantic import EmailStr
from .prefix_id import PrefixId
from . import utils
from .database import Base, Filters, Page, BaseIO


class UserId(PrefixId):
    prefix = "user"


class UserCreateAttrs(BaseIO):
    name: str
    email: EmailStr


class UserUpdateAttrs(BaseIO):
    name: Optional[str]
    email: Optional[EmailStr]


class AuditWhenMixin:
    created_at = Column(DateTime(True), nullable=False, default=utils.get_utc_now)
    updated_at = Column(DateTime(True), nullable=False, onupdate=utils.get_utc_now)
    deleted_at = Column(DateTime(True), nullable=True)


class AuditByMixin:
    created_by = Column(String(True), nullable=False, default=utils.get_utc_now)
    updated_by = Column(String(50), nullable=False)
    update_request = Column(String(50), nullable=False)


class AuditMixin(AuditWhenMixin, AuditByMixin):
    ...


I = TypeVar("I", bound=PrefixId)


class IdMixin(Generic[I]):
    id: I = cast(I, Column(String(50), primary_key=True, unique=True))


def make_user_audit_id(user_id: UserId, type: str = "self"):
    return f"{type}:{user_id}"


class User(AuditMixin, IdMixin[UserId], Base):
    __versioned__ = {}  # hooks up versioning
    __tablename__ = "Users"

    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    secret = Column(String(50), nullable=False)

    @classmethod
    def create(cls, *, attrs: UserCreateAttrs, request_id: str):
        id = UserId.make()
        secret = str(uuid.uuid4())
        now = utils.get_utc_now()
        return cls(
            id=id,
            name=attrs.name,
            email=attrs.email,
            secret=secret,
            created_by=make_user_audit_id(id),
            updated_by=make_user_audit_id(id),
            update_request=request_id,
            updated_at=now,
            created_at=now,
        )

    def update(self, *, attrs: UserUpdateAttrs, request_id: str, updated_by: str):
        if attrs.name != None:
            self.name = attrs.name
        if attrs.email != None:
            self.email = attrs.email

        self.update_request = request_id
        self.updated_by = make_user_audit_id(self.id)
        self.updated_at = utils.get_utc_now()

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
        db_session: database.Session,
    ) -> Page["User"]:
        q = db_session.query(cls).filter(*filters).order_by(cls.created_at, cls.id)
        page, prev_page, next_page = database.page_query_results(q, pagination_params)
        return Page(prev_key=prev_page, items=page, next_key=next_page)

    @classmethod
    def use_email_filter(cls, email: EmailStr = None) -> database.Filters:
        if email is None:
            return []
        return [cls.email == email]  # type: ignore

    def delete(self, request_id: str):
        self.updated_by = make_user_audit_id(self.id)
        self.update_request = request_id
        self.deleted_at = utils.get_utc_now()
        self.updated_at = utils.get_utc_now()
