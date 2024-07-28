"""This module contains functions that interact with the database."""

# pylint: disable=missing-function-docstring

from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session

from app.database.schemas import User


def get_user_by_username(username: str, db_session: Session) -> Row[tuple[int]] | None:
    return db_session.query(User.id).filter(User.username == username).first()


def populate_user_table():
    pass
