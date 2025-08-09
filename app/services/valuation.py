from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.structure_settings import StructureSettings
from app.models.item_value import ItemValue
from app.models.item import Item

def get_currency_item_for_structure(db: Session, structure_id: str):
    ss = db.query(StructureSettings).filter(StructureSettings.structure_id == structure_id).first()
    return ss.currency_item_id if ss and ss.currency_item_id else None

def get_item_value_at(db: Session, structure_id: str, item_id: int, at: datetime) -> Decimal | None:
    row = (
        db.query(ItemValue)
        .filter(
            ItemValue.structure_id == structure_id,
            ItemValue.item_id == item_id,
            ItemValue.effective_from <= at,
        )
        .order_by(ItemValue.effective_from.desc())
        .first()
    )
    if not row:
        return None
    return Decimal(row.value_in_currency)

def value_of_item(db: Session, structure_id: str, item_id: int, qty: int, at: datetime) -> Decimal | None:
    v = get_item_value_at(db, structure_id, item_id, at)
    return None if v is None else v * Decimal(qty)
