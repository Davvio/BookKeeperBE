import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.core.database import SessionLocal
from app.core.security import decode_jwt_token
from app.models.user import User

# simple logger
logger = logging.getLogger("bookkeeper.deps")
logger.setLevel(logging.INFO)

oauth2_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    token_str = token.credentials
    try:
        payload = decode_jwt_token(token_str)
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(401, "Invalid token")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(401, "Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

def get_current_structure(user: User = Depends(get_current_user)) -> str:
    return user.structure_id
