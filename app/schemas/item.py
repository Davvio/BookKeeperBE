from pydantic import BaseModel, conint, constr
from typing import Optional, Literal

class ItemCreate(BaseModel):
    name: constr(min_length=2, max_length=120)
    category: constr(min_length=2, max_length=50)
    stack_size: conint(ge=1, le=999) = 64
    is_active: bool = True

class ItemUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=120)] = None
    category: Optional[constr(min_length=2, max_length=50)] = None
    stack_size: Optional[conint(ge=1, le=999)] = None
    is_active: Optional[bool] = None

class ItemOut(BaseModel):
    id: int
    name: str
    code: str
    category: str
    stack_size: int
    is_active: bool
    class Config: from_attributes = True
