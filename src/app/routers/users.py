# pylint: disable=missing-docstring,fixme

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.database_handler import get_user_by_username, get_user_credentials
from app.settings.environments import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    HASHING_ALGORITHM,
    SECRET_KEY,
)
from app.utils.dependencies import database_session

from .exceptions import CredentialsException
from .models import Token, TokenData

# users_router = APIRouter(prefix="/api/users", tags=["users"])  # FIXME: prefix
users_router = APIRouter(tags=["users"])

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.post("/token")
async def login(
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


@users_router.get("/current_user")
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Annotated[Session, Depends(database_session)],
):
    token_data = verify_access_token(token=token, db_session=db_session)
    return token_data


def create_access_token(data: dict, expiration_delta: timedelta | None) -> str:
    data_to_encode = data.copy()
    if expiration_delta:
        expire = datetime.now(timezone.utc) + expiration_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, key=SECRET_KEY, algorithm=HASHING_ALGORITHM  # type: ignore
    )
    return encoded_jwt


def verify_access_token(token: str, db_session: Session) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])  # type: ignore
        username: str = payload.get("sub")
        if not username:
            raise CredentialsException(detail="Could not validate credentials")
        token_data = TokenData(username=username)
    except InvalidTokenError as exc:
        raise CredentialsException(detail="Invalid token") from exc
    user = get_user_by_username(username=token_data.username, db_session=db_session)  # type: ignore
    if not user:
        raise CredentialsException(detail="User not found")
    return token_data


def generate_hashed_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, plain_password: str, db_session: Session):
    user = get_user_credentials(db_session=db_session, username=username)
    if user is None:
        return False
    if not verify_hashed_password(plain_password, user.hashed_password):
        return False
    return user
