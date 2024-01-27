from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.database.settings import local_session

def database_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")