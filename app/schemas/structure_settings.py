from pydantic import BaseModel
from typing import Optional

class StructureSettingsOut(BaseModel):
    structure_id: str
    currency_item_id: Optional[int] = None
    currency_item_name: Optional[str] = None

class SetCurrencyIn(BaseModel):
    currency_item_id: int
