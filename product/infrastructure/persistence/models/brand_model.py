import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, UUID
from infrastructure.persistence.database.database import Base

if TYPE_CHECKING:
    from infrastructure.persistence.models.product_model import ProductModel


class BrandModel(Base):
    __tablename__ = "brand"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel", back_populates="brand", cascade="all, delete"
    )
    
