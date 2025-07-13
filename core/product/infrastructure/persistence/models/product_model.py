import uuid
from infrastructure.persistence.database import Base
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, TYPE_CHECKING
from sqlalchemy import UUID, ForeignKey
from infrastructure.persistence.models.association_models import (
    AssociationProductCategoryModel,
    AssosiationProductAttributeModel
)


if TYPE_CHECKING:
    from infrastructure.persistence.models.brand_model import BrandModel
    from infrastructure.persistence.models.category_model import CategoryModel
    from infrastructure.persistence.models.image_model import ProductImageModel
    from infrastructure.persistence.models.attribute_model import AttributeModel


class ProductModel(Base):
    __tablename__ = "product"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("brand.id"))
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships one-to-many
    brand: Mapped["BrandModel"] = relationship("BrandModel", back_populates="products")
    
    # Relationships many-to-one
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
    attributes: Mapped[List["AttributeModel"]] = relationship(
        "AttributeModel",
        secondary=AssosiationProductAttributeModel.__table__,
        back_populates="product",
        lazy="joined"
    )
