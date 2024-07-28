
# pylint: disable=missing-docstring

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database_handler import get_user_by_username
from app.utils.dependencies import database_session

from .models import UserMaker

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@users_router.post("/create_user/")
async def create_user(
    user_info: Annotated[UserMaker, Body()],
    db_session: Session = Depends(database_session)
):
    user = get_user_by_username(username=user_info.username,
                                db_session=db_session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"username {user_info.username} already existed"
        )
    return True

@users_router.get("/", response_model=list[UserMaker])
async def get_users():
    pass
