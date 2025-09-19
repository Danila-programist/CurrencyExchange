from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserRequest(UserBase):
    password: str

class UserDatabase(UserBase):
    hashed_password: str