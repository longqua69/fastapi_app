from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    fullname: str | None = None
    email: str | None = None

class UserMaker(UserBase):
    pass

class User(UserBase):
    id: int
    hashed_password: str

class ItemMaker(BaseModel):
    name: str

class Item(ItemMaker):
    id: int
    user_id: int
