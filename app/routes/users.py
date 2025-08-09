# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.deps import get_db, get_current_user
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

def ensure_admin(u: User):
    if u.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin only")

@router.post("", response_model=UserOut, status_code=201)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_admin(current_user)

    exists = db.query(User).filter(User.username == payload.username).first()
    if exists:
        raise HTTPException(status_code=409, detail="Username already exists")

    new_user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,                                # any role allowed
        structure_id=current_user.structure_id,           # force same structure
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_admin(current_user)
    users = (
        db.query(User)
        .filter(User.structure_id == current_user.structure_id)
        .order_by(User.username.asc())
        .all()
    )
    return users
