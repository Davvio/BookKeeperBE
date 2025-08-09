from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from app.core.database import Base

class ItemCategory(Base):
    __tablename__ = "item_categories"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)   # e.g. "ingot"
    name = Column(String(100), nullable=False)               # e.g. "Ingot"

    __table_args__ = (
        UniqueConstraint("code", name="uq_item_categories_code"),
    )
