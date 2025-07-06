import uuid
import decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Integer, DECIMAL, ForeignKey
from infrastructure.persistence.models.base import Base
from infrastructure.persistence.models.order_model import Order


class OrderItem(Base):
    __tablename__ = "order_item"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL, nullable=False)

    order: Mapped[Order] = relationship(back_populates="items")
