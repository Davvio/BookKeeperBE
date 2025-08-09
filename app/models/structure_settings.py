from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class StructureSettings(Base):
    __tablename__ = "structure_settings"

    structure_id = Column(String(50), primary_key=True)   # same type you use elsewhere
    currency_item_id = Column(Integer, ForeignKey("items.id"), nullable=True)

    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    currency_item = relationship("Item", lazy="joined")
    updater = relationship("User")
