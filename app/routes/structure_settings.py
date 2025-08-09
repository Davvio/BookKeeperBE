from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.deps import get_db, get_current_user
from app.models.user import User
from app.models.structure_settings import StructureSettings
from app.models.item import Item
from app.schemas.structure_settings import StructureSettingsOut, SetCurrencyIn

router = APIRouter(prefix="/structure-settings", tags=["structure-settings"])

def ensure_admin(u: User):
    if u.role != "ADMIN":
        raise HTTPException(403, "Admin only")

@router.get("", response_model=StructureSettingsOut)
def get_settings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ss = db.query(StructureSettings).get(user.structure_id)
    if not ss:
        ss = StructureSettings(structure_id=user.structure_id)
        db.add(ss); db.commit(); db.refresh(ss)
    name = ss.currency_item.name if ss.currency_item_id else None
    return StructureSettingsOut(structure_id=ss.structure_id, currency_item_id=ss.currency_item_id, currency_item_name=name)

@router.put("/currency", response_model=StructureSettingsOut)
def set_currency(payload: SetCurrencyIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_admin(user)
    item = db.query(Item).get(payload.currency_item_id)
    if not item or not item.is_active:
        raise HTTPException(400, "Invalid currency item")
    ss = db.query(StructureSettings).get(user.structure_id)
    if not ss:
        ss = StructureSettings(structure_id=user.structure_id)
        db.add(ss)
    ss.currency_item_id = item.id
    ss.updated_by_user_id = user.id
    db.commit(); db.refresh(ss)
    return StructureSettingsOut(structure_id=ss.structure_id, currency_item_id=ss.currency_item_id, currency_item_name=item.name)
