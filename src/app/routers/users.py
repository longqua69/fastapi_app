# pylint: disable=missing-docstring,fixme

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.settings.environments import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.authentication import (
    authenticate_user,
    create_access_token,
    verify_access_token,
)
from app.utils.dependencies import database_session, oauth2_scheme

from .models import Token

# users_router = APIRouter(prefix="/api/users", tags=["users"])  # FIXME: prefix
users_router = APIRouter(tags=["users"])


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
