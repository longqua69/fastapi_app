"""Database schemas for the application."""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .settings import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    fullname: Mapped[str | None]
    email: Mapped[str | None]

class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    user_id = mapped_column(ForeignKey("user.id"))
