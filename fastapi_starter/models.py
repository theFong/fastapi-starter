from typing import cast
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from pydantic import EmailStr
from .prefix_id import PrefixId
from . import utils

Base = declarative_base()
metadata = Base.metadata


class UserId(PrefixId):
    prefix = "user"
    ...


class User(Base):
    __tablename__ = "Users"

    id: PrefixId = cast(PrefixId, Column(String(50), primary_key=True, unique=True))
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    create_date = Column(DateTime(True), nullable=False)

    @classmethod
    def create(cls, *, name: str, email: EmailStr):
        id = UserId.make()
        now = utils.get_utc_now()
        return cls(id=id, name=name, email=email, create_date=now)
