import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String
from infrastructure.persistence.database.database import Base

if TYPE_CHECKING:
    from infrastructure.persistence.models.attribute_model import AttributeModel
    from infrastructure.persistence.models.product_model import ProductModel


class AssociationProductCategoryModel(Base):
    __tablename__ = "association_product_category"
    
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("category.id"), primary_key=True)


class AssosiationProductAttributeModel(Base):
    __tablename__ = "association_product_attribute"
    
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
    attribute_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("attributes.id"), primary_key=True)
    value: Mapped[str] = mapped_column(String)

    product: Mapped["ProductModel"] = relationship(
        "ProductModel",
        back_populates="attribute_links"
    )
    attribute: Mapped["AttributeModel"] = relationship(
        "AttributeModel",
        back_populates="product_links"
    )