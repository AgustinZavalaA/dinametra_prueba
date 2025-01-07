from datetime import timedelta
from datetime import datetime, timezone
from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User
from jose import jwt

from database import LocalSession

router = APIRouter(prefix="", tags=["auth"])

# We need to hide this key to be complete secure, but as this needs to be pushed to github I decided to place it here
# generated using : https://jwtsecret.com/generate
SECRET_KEY = "01f1e1ec19d4796fb38f6424cc653cd094b574ebf64277487bde4c846b28a8d4247ec481807d63b31bf014d85573e118026ff64f7cf4ad74955105107ac55b1bfc7a5f1f66c0098aca219d0c79723d116f160863992643fc73dcf31feb53cd05cee96f16968895605e99b5c1df439cf0031386b05fdc6831cb3d86801cb9c823157c0e5ec73913457116c531caf071a61159620366cdc5ad309e178bc27f760a2f87d0bc8c18ce74b2a87550db1a84c6db7357d358b0a40184ba0af816d2457d9276498f6517f0b449aa5ee36fd09eea345145395cf467c002275fffdf952c198beb58f1b12fc355549550a36ac1254665a0ff69f610e58aa320cfa6b39eddf3"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# get db with context manager, so it closes itself if it encounters an exception or when the db is no longer being used
def get_db():
    with LocalSession() as db:
        yield db


# dependency injection, we inject the db connection to the endpoints that need it
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)

    db.commit()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
) -> dict:
    user: bool | User = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password does not match"
        )

    token = create_access_token(user.email, user.id, timedelta(minutes=10))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not found"
        )
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password does not match"
        )

    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {
        "sub": email,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
