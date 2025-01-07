from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from models import User

from database import LocalSession
from auth import get_current_user

router = APIRouter(prefix="", tags=["tasks"])

#
# class CreateUserRequest(BaseModel):
#    email: str
#    password: str


# class Token(BaseModel):
#    access_token: str
#    token_type: str


# get db with context manager, so it closes itself if it encounters an exception or when the db is no longer being used
def get_db():
    with LocalSession() as db:
        yield db


# dependency injection, we inject the db connection to the endpoints that need it
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/tasks")
async def get_user_tasks(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="Not logged in")
    user_db = db.query(User).filter(User.id == user.get("id")).first()

    if not user_db:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="User not found in DB")

    return user_db.tasks
