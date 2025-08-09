# app/routes/trades.py
import json
from datetime import timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.trade import TradeLogCreate, TradeLogOut
from app.models.trade import Trade
from app.models.user import User as UserModel
from app.services.deps import get_db, get_current_user
from app.models.user import User
from app.services.valuation import get_currency_item_for_structure, get_item_value_at

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
        to_location=dbt.to_location,
        actor_user_id=current_user.id,         # NEW
        actor_username=current_user.username,  # NEW
    )

@router.get("/", response_model=list[TradeLogOut])
def get_trades(
    player: str | None = Query(None, description="actor userId (number) or username"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Trade).filter(Trade.structure_id == current_user.structure_id)

    # Non-admins only see their own
    if current_user.role != "ADMIN":
        q = q.filter(Trade.user_id == current_user.id)
    else:
        # Optional filter by actor (user_id or username) — admin only
        if player:
            if player.isdigit():
                q = q.filter(Trade.user_id == int(player))
            else:
                q = q.join(UserModel).filter(UserModel.username == player)

    trades = q.order_by(Trade.timestamp.desc()).all()
    out = []
    # Per mappare nome->id una volta sola (case-insensitive)
    all_items = db.query(Item).all()
    item_by_name = {i.name.lower(): i.id for i in all_items}

    for t in trades:
        profit = Decimal("0")
        unpriced = False

        currency_item_id = get_currency_item_for_structure(db, t.structure_id)
        currency_name = None
        if currency_item_id:
            ci = db.query(Item).get(currency_item_id)
            currency_name = ci.name if ci else None

        trade_time = t.timestamp if t.timestamp.tzinfo else t.timestamp.replace(tzinfo=timezone.utc)

        def add_value(entries, sign):
            nonlocal profit, unpriced
            for e in entries:
                nm = (e.get("name") or "").lower()
                qty = int(e.get("quantity") or 0)
                item_id = item_by_name.get(nm)
                if not item_id or qty <= 0:
                    unpriced = True
                    continue
                val = get_item_value_at(db, t.structure_id, item_id, trade_time)
                if val is None:
                    unpriced = True
                else:
                    profit += sign * val * Decimal(qty)

        add_value(json.loads(t.items_gained), Decimal("1"))
        add_value(json.loads(t.items_given), Decimal("-1"))

        out.append(TradeLogOut(
            id=t.id,
            timestamp=t.timestamp.isoformat(),
            items_given=json.loads(t.items_given),
            items_gained=json.loads(t.items_gained),
            from_location=t.from_location,
            to_location=t.to_location,
            actor_user_id=t.user_id,
            actor_username=t.user.username if t.user else "",
            profit=str(profit) if currency_item_id else None,
            currency_item_name=currency_name,
            unpriced=unpriced or (currency_item_id is None),
        ))
    return out
