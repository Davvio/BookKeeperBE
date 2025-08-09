from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, func, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.core.database import Base

class ItemValue(Base):
    __tablename__ = "item_values"

    id = Column(Integer, primary_key=True)
    structure_id = Column(String(50), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    value_in_currency = Column(Numeric(20, 6), nullable=False)  # 0.001 .. 1_000_000 (CHECK in alembic)
    effective_from = Column(DateTime(timezone=True), nullable=False)

    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    item = relationship("Item", lazy="joined")
    creator = relationship("User")

    __table_args__ = (
        UniqueConstraint("structure_id", "item_id", "effective_from", name="uq_item_values_hist"),
        Index("ix_item_values_lookup", "structure_id", "item_id", "effective_from"),
    )
