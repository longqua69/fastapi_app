"""This module contains the dependencies used in the FastAPI application."""

# pylint: disable=missing-function-docstring
from fastapi.security import OAuth2PasswordBearer

from app.database.settings import local_session


def database_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
