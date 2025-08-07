from pydantic import BaseModel
from typing import Literal

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: Literal["EMPLOYEE", "ADMIN"] = "EMPLOYEE"

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    structure_id: str

    class Config:
        from_attributes = True
