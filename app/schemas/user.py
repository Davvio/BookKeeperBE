# app/schemas/user.py
from pydantic import BaseModel, constr
from typing import Literal

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)
    role: Literal["EMPLOYEE", "ADMIN", "GUILDMASTER"]

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    structure_id: str

    class Config:
        from_attributes = True
