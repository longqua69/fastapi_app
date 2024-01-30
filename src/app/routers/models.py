from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    fullname: str | None = None
    email: str | None = None

class UserMaker(UserBase):
    plain_password: str

class User(UserBase):
    id: int
    hashed_password: str

class ItemMaker(BaseModel):
    name: str

class Item(ItemMaker):
    id: int
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
