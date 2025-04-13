from infrastructure.persistence.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UUID
import uuid


class AssociationProductCategoryModel(Base):
    __tablename__ = "association_product_category"
    
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("product.id"), primary_key=True)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("category.id"), primary_key=True)
