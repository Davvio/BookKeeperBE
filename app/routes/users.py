from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.core.security import hash_password
from app.services.deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    if me.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username taken")

    u = User(
        username=data.username,
        hashed_password=hash_password(data.password),
        role=data.role,
        structure_id=me.structure_id
    )
    db.add(u); db.commit(); db.refresh(u)
    return u
