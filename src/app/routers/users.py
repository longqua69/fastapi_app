from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .models import UserBase

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@users_router.post("/create_user")
async def create_user(
    user_info: Annotated[UserBase, Body()]
):
    return user_info

@users_router.get("/", response_model=list[UserBase])
async def get_users():
    pass

