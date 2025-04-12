
from sqlalchemy import String, DECIMAL, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any, List, TYPE_CHECKING
from uuid import UUID
from domain.value_objects.product_attribute import ProductAttribute
from infrastructure.persistence.database import Base

if TYPE_CHECKING:
    from infrastructure.persistence.models.brand_model import BrandModel
    from infrastructure.persistence.models.category_model import CategoryModel
    

class ProductModel(Base):
    __tablename__ = "product"
    
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    brand_id: Mapped[UUID] = mapped_column(ForeignKey("brand.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    attributes: Mapped[List[ProductAttribute]] = mapped_column(ARRAY(String(255)))
    
    # Relationships many-to-one
    brand: Mapped["BrandModel"] = relationship("BrandModel", back_populates="products")

    # Relationships many-to-many
    categories: Mapped[List["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary="association_product_category",
        back_populates="products",
        lazy="joined",
    )
