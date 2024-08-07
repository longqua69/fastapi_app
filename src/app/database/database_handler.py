"""This module contains functions that interact with the database."""

# pylint: disable=missing-function-docstring,fixme

from sqlalchemy.orm import Session

from app.database.schemas import User


def get_user_by_username(username: str, db_session: Session):
    # TODO: Refactor to follow new change in sqlalchemy 2.0
    return db_session.query(User.id).filter(User.username == username).one_or_none()


def get_user_credentials(username: str, db_session: Session):
    # TODO: Refactor to follow new change in sqlalchemy 2.0
    return (
        db_session.query(User.username, User.hashed_password)
        .filter(User.username == username)
        .one_or_none()
    )


def populate_user_table():
    pass
