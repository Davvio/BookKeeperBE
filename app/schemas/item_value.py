from pydantic import BaseModel, condecimal, validator
from typing import Optional
from datetime import datetime, timezone

class ItemValueCreate(BaseModel):
    item_id: int
    value_in_currency: condecimal(gt=0, max_digits=20, decimal_places=6)
    effective_from: Optional[datetime] = None

    @validator("value_in_currency")
    def value_range(cls, v):
        if v < 0.001 or v > 1_000_000:
            raise ValueError("value_in_currency out of allowed range (0.001 .. 1_000_000)")
        return v

    @validator("effective_from", pre=True, always=True)
    def default_now(cls, v):
        return v or datetime.now(timezone.utc)

class ItemValueOut(BaseModel):
    id: int
    structure_id: str
    item_id: int
    value_in_currency: str
    effective_from: datetime
    class Config: from_attributes = True
