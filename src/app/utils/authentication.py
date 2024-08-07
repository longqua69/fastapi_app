# pylint: disable=missing-docstring

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.database.database_handler import get_user_by_username, get_user_credentials
from app.routers.models import TokenData
from app.settings.environments import HASHING_ALGORITHM, SECRET_KEY
from app.utils.dependencies import password_context

from .exceptions import CredentialsException


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
