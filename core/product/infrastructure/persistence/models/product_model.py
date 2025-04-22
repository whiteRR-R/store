
from domain.entities.product import Product
from domain.value_objects.product_attribute import ProductAttribute
from infrastructure.persistence.database import Base
from sqlalchemy import String, DECIMAL, Integer, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any, List, Dict, TYPE_CHECKING
from sqlalchemy import UUID
import uuid


if TYPE_CHECKING:
    from infrastructure.persistence.models.brand_model import BrandModel
    from infrastructure.persistence.models.category_model import CategoryModel
    

class ProductModel(Base):
    __tablename__ = "product"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    brand_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("brand.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    attributes: Mapped[Dict[str, str]] = mapped_column(JSONB, nullable=False)
    
    # Relationships many-to-one
    brand: Mapped["BrandModel"] = relationship("BrandModel", back_populates="products")

    # Relationships many-to-many
    categories: Mapped[List["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary="association_product_category",
        back_populates="products",
        lazy="joined",
    )

    def __init__(self, product: Product):
        self.id = product.id
        self.brand_id = product.brand_id
        self.name = product.name
        self.description = product.description
        self.price = product.price
        self.attributes = {k: v.value for k, v in product.attributes.items()}
