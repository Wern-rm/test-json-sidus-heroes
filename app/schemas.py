from pydantic import BaseModel


class UserUpdate(BaseModel):
    new_login: str
    new_name: str


class UserCreate(BaseModel):
    login: str
    name: str
    password: str