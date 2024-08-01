"""Module to define the database settings."""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.settings.environments import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

CONNECTION_STR = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(CONNECTION_STR, echo=True)

local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
