# pylint: disable=missing-docstring

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.database_handler import get_user_by_username, get_user_credentials
from app.settings.environments import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    HASHING_ALGORITHM,
    SECRET_KEY,
)
from app.utils.dependencies import database_session

from .models import Token, UserMaker

users_router = APIRouter(prefix="/api/users", tags=["users"])

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.post("/token")
async def login_to_get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(database_session)],
) -> Token:
    user_credentials = authenticate_user(
        form_data.username, form_data.password, db_session=db_session
    )
    if not user_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expiration_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_credentials.username},
        expiration_delta=access_token_expiration_delta,
    )
    return Token(access_token=access_token, token_type="bearer")


def create_access_token(data: dict, expiration_delta: timedelta | None) -> str:
    data_to_encode = data.copy()
    if expiration_delta:
        expire = datetime.now(timezone.utc) + expiration_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, key=SECRET_KEY, algorithm=HASHING_ALGORITHM
    )
    return encoded_jwt


def generate_hashed_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def authenticate_user(
    username: str, plain_password: str, db_session: Session = database_session
):
    user = get_user_credentials(db_session=db_session, username=username)
    if user is None:
        return False
    if not verify_hashed_password(plain_password, user.hashed_password):
        return False
    return user


@users_router.post("/create_user/")
async def create_user(
    user_info: Annotated[UserMaker, Body()],
    db_session: Session = Depends(database_session),
):
    user = get_user_by_username(username=user_info.username, db_session=db_session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"username {user_info.username} already existed",
        )
    # return Token


@users_router.get("/", response_model=list[UserMaker])
async def get_users():
    # TODO: Refactor this path operation
    pass
