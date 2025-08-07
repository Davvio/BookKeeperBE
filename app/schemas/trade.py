from pydantic import BaseModel
from typing import List

class TradeItem(BaseModel):
    name: str
    quantity: int

class TradeLogCreate(BaseModel):
    items_given: List[TradeItem]
    items_gained: List[TradeItem]
    from_location: str
    to_location: str

class TradeLogOut(BaseModel):
    id: int
    timestamp: str
    items_given: List[TradeItem]
    items_gained: List[TradeItem]
    from_location: str
    to_location: str

    class Config:
        from_attributes = True
