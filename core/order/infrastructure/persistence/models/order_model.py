import uuid
from typing import List, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from sqlalchemy import String, DECIMAL, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.persistence.models.base import Base

if TYPE_CHECKING:
    from infrastructure.persistence.models.order_item_model import OrderItem


class Order(Base): 
    __tablename__ = "order"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    total: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[String] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    shipped_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
