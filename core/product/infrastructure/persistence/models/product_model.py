from infrastructure.persistence.database import Base
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, TYPE_CHECKING
from sqlalchemy import UUID, ForeignKey
from infrastructure.persistence.models.association_models import AssociationProductCategoryModel
from infrastructure.persistence.models.image_model import ProductImageModel
import uuid


if TYPE_CHECKING:
    from infrastructure.persistence.models.brand_model import BrandModel
    from infrastructure.persistence.models.category_model import CategoryModel


class ProductModel(Base):
    __tablename__ = "product"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("brand.id"))
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    attributes: Mapped[Dict[str, str]] = mapped_column(JSONB, nullable=False)
    
    # Relationships many-to-one
    brand: Mapped["BrandModel"] = relationship("BrandModel", back_populates="products")
    images: Mapped[List["ProductImageModel"]] = relationship(
        "ProductImageModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    # Relationships many-to-many
    categories: Mapped[List["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary=AssociationProductCategoryModel.__table__,
        back_populates="products",
        lazy="joined",
    )
