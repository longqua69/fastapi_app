import uvicorn
from fastapi import FastAPI

from app.routers.users import users_router

from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import (
    APIRouter,
    Body,
    Depends,
    status,
    HTTPException
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.utils.dependencies import database_session
from app.database.database_handler import get_user_by_username, get_user_credentials
from app.routers.models import UserMaker, UserBase, Token, TokenData

app = FastAPI(
    title="Mini app to learn FastAPI",
    version="0.0.1",
)

app.include_router(users_router)

@app.get("/")
async def root():
    return {"Hello": "Mom"}

SECRET_KEY = "d686fa3270f634cc3619fc5edfd67f44565439af6ec2b4a904d14e5d75240d34"
HASHING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_to_get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(database_session)]
) -> Token:
    user_credentials = authenticate_user(form_data.username,
                                         form_data.password,
                                         db_session=db_session)
    if not user_credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expiration_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_credentials.username},
        expiration_delta=access_token_expiration_delta
    )
    return Token(access_token=access_token, token_type="bearer")

def create_access_token(data: dict, expiration_delta: timedelta | None) -> str:
    data_to_encode = data.copy()
    if expiration_delta:
        expire = datetime.now(timezone.utc) + expiration_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode,
                             key=SECRET_KEY,
                             algorithm=HASHING_ALGORITHM)
    return encoded_jwt

def generate_hashed_password(plain_password: str) -> str:
    return password_context.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def authenticate_user(username: str,
                      plain_password: str,
                      db_session: Session = database_session):
    user = get_user_credentials(db_session=db_session, username=username)
    if user is None:
        return False
    if not verify_hashed_password(plain_password, user.hashed_password):
        return False
    return user

@app.get("/current_user", response_model=UserBase)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Session = Depends(database_session) # FIXME: Review Dependencies session to check this and revise if need
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try: 
        payload = jwt.decode(token=token,
                            key=SECRET_KEY,
                            algorithms=HASHING_ALGORITHM)
        if username := payload.get("sub") is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db_session=db_session,
                                username=token_data)
    if user is None:
        raise credentials_exception
    return user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)