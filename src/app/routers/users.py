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
from .models import UserMaker, UserBase, Token, TokenData

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@users_router.get("/")
async def get_users():
    # TODO: Refactor this path operation
    pass

