import uuid
from typing import TYPE_CHECKING
from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.persistence.database import Base

if TYPE_CHECKING:
    from infrastructure.persistence.models.product_model import ProductModel


class ProductImageModel(Base):
    __tablename__ = "product_image"
    
    id: Mapped[UUID] = mapped_column(UUID, default=uuid.uuid4, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),nullable=False,)
    url: Mapped[str] = mapped_column(String(), nullable=False)
    
    product: Mapped["ProductModel"] = relationship("ProductModel", back_populates="images")
