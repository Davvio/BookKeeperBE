import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.trade import TradeLogCreate, TradeLogOut
from app.models.trade import Trade
from app.services.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TradeLogOut)
def create_trade(
    trade: TradeLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dbt = Trade(
        user_id=current_user.id,
        structure_id=current_user.structure_id,
        items_given=json.dumps([i.dict() for i in trade.items_given]),
        items_gained=json.dumps([i.dict() for i in trade.items_gained]),
        from_location=trade.from_location,
        to_location=trade.to_location,
    )
    db.add(dbt); db.commit(); db.refresh(dbt)
    return TradeLogOut(
        id=dbt.id,
        timestamp=dbt.timestamp.isoformat(),
        items_given=json.loads(dbt.items_given),
        items_gained=json.loads(dbt.items_gained),
        from_location=dbt.from_location,
        to_location=dbt.to_location
    )

@router.get("/", response_model=list[TradeLogOut])
def get_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Trade).filter(Trade.structure_id == current_user.structure_id)
    if current_user.role != "ADMIN":
        q = q.filter(Trade.user_id == current_user.id)
    trades = q.order_by(Trade.timestamp.desc()).all()
    return [
        TradeLogOut(
            id=t.id,
            timestamp=t.timestamp.isoformat(),
            items_given=json.loads(t.items_given),
            items_gained=json.loads(t.items_gained),
            from_location=t.from_location,
            to_location=t.to_location
        )
        for t in trades
    ]
