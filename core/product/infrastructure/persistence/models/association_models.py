import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UUID, String
from infrastructure.persistence.database import Base


class AssociationProductCategoryModel(Base):
    __tablename__ = "association_product_category"
    
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("category.id"), primary_key=True)


class AssosiationProductAttributeModel(Base):
    __tablename__ = "association_product_attribute"
    
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
    attribute_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("attributes.id"), primary_key=True)
    value: Mapped[uuid.UUID] = mapped_column(String)
