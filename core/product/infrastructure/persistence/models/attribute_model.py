import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, ForeignKey
from infrastructure.persistence.database.database import Base
from infrastructure.persistence.models.association_models import AssosiationProductAttributeModel


if TYPE_CHECKING:
    from infrastructure.persistence.models.product_model import ProductModel


class AttributeModel(Base):
    __tablename__ = "attributes"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        secondary=AssosiationProductAttributeModel.__table__,
        back_populates="attributes"
    )
    