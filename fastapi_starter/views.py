from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, status, exceptions

from . import database
from . import models
from . import utils


users = APIRouter(prefix="/users", tags=["Users"])


class UserResp(BaseModel):
    class Config:
        orm_mode = True

    id: models.UserId
    name: str
    email: EmailStr
    create_date: datetime


class ManyUseResp(BaseModel):
    users: List[UserResp]


@users.get("", response_model=ManyUseResp)
def get_users(db_session: database.Session = Depends(database.use_session)):
    res = db_session.query(models.User).all()
    return ManyUseResp(users=res)


@users.get("/{user_id}", response_model=UserResp)
def get_user_by_id(
    id: models.UserId, db_session: database.Session = Depends(database.use_session)
):
    resp = db_session.query(models.User).get(id)
    if resp is None:
        raise exceptions.HTTPException(400, "User does not exist")
    return resp


class CreateUserAttrs(BaseModel):
    name: str
    email: EmailStr


@users.post("", response_model=UserResp, status_code=status.HTTP_201_CREATED)
def create_user(
    create_attrs: CreateUserAttrs,
    db_session: database.Session = Depends(database.use_session),
):
    with utils.handle_constraint_error(), db_session.begin():
        user = models.User.create(**create_attrs.dict())
        db_session.add(user)
    return user
