from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.models.user import User
from app.core.security import verify_password, create_jwt_token
from app.services.deps import get_db

router = APIRouter()

@router.post("/auth/login")
def login(form: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_jwt_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "structure_id": user.structure_id,
    })
    return {"access_token": token, "token_type": "bearer", "role": user.role}
