from fastapi import Depends

from app.database.settings import local_session


def database_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()