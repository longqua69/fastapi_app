"""This module contains the dependencies used in the FastAPI application."""

# pylint: disable=missing-function-docstring

from app.database.settings import local_session

def database_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()
