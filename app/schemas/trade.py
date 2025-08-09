from pydantic import BaseModel
from typing import List, Optional


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
    actor_user_id: int
    actor_username: Optional[str] = ""

    # NEW:
    profit: Optional[str] = None              # string per Decimal->JSON
    currency_item_name: Optional[str] = None  # es. "Iron Ingot"
    unpriced: bool = False                    # true se mancano valutazioni

    class Config:
        from_attributes = True
