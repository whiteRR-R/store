import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.persistence.models.base import Base


if TYPE_CHECKING:
    from infrastructure.persistence.models.user_model import UserModel


class AddressModel(Base):
    __tablename__ = "address"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    street: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    apartment: Mapped[str] = mapped_column(String(20), nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="addresses")
