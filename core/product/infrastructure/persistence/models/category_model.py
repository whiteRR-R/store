import uuid
from typing import List, Any, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.persistence.database.database import Base
from infrastructure.persistence.models.association_models import AssociationProductCategoryModel


if TYPE_CHECKING:
    from infrastructure.persistence.models.product_model import ProductModel


class CategoryModel(Base):
    __tablename__ = "category"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relationships many-to-many
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        secondary=AssociationProductCategoryModel.__table__,
        back_populates="categories"
    )
    
