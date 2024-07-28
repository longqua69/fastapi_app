"""Module to define the database settings."""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

USER = "postgres"
PASSWORD = "example"
HOST = "localhost"
PORT = "5432"
DATABASE = "mydb"
CONNECTION_STR = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(CONNECTION_STR, echo=True)

local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
