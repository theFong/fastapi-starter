from datetime import datetime
from sqlalchemy import util

from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import user
from starlette.responses import Response
from fastapi_starter import pagination
from typing import List
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, status, exceptions

from . import database
from . import models
from . import utils


users = APIRouter(prefix="/users", tags=["Users"])


class UserResp(database.IOBase):
    id: models.UserId
    name: str
    email: EmailStr
    create_date: datetime
    update_date: datetime


@users.get("", response_model=pagination.PageResponse[UserResp])
def get_users(
    email_filter: database.Filters = Depends(models.User.use_email_filter),
    pagination_params: pagination.PaginationParams = Depends(pagination.use_params),
    db_session: database.Session = Depends(database.use_session),
):
    return models.User.get_many(
        pagination_params=pagination_params, filters=email_filter, db_session=db_session
    )


@users.get("/{user_id}", response_model=UserResp)
def get_user_by_id(
    id: models.UserId, db_session: database.Session = Depends(database.use_session)
):
    user = models.User.get_by_id(id=id, db_session=db_session)
    if user is None:
        raise exceptions.HTTPException(400, "User does not exist")
    return user


@users.post("", response_model=UserResp, status_code=status.HTTP_201_CREATED)
def create_user(
    create_attrs: models.UserCreateAttrs,
    db_session: database.Session = Depends(database.use_session),
):
    with utils.handle_constraint_error(), db_session.begin():
        user = models.User.create(attrs=create_attrs)
        db_session.add(user)
    return user


@users.put("/{user_id}", response_model=UserResp)
def update_user_by_id(
    id: models.UserId,
    update_attrs: models.UserUpdateAttrs,
    db_session: database.Session = Depends(database.use_session),
):
    change_set = models.User.update(attrs=update_attrs)

    with utils.handle_constraint_error(), db_session.begin():
        db_session.query(models.User).filter(models.User.id == id).update(change_set)
        user = models.User.get_by_id(id=id, db_session=db_session)
        if user is None:
            raise exceptions.HTTPException(400, "User does not exist")
        return user


@users.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(
    id: models.UserId,
    db_session: database.Session = Depends(database.use_session),
):
    with utils.handle_constraint_error(), db_session.begin():
        res = db_session.query(models.User).filter(models.User.id == id).delete()
        if res ==0:
            raise exceptions.HTTPException(400, "User does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
