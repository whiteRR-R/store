from decimal import Decimal
from math import prod
from typing import Any
from sqlalchemy import String, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from domain.entities.product import Product
from infrastructure.persistence.database import Base


class ProductModel(Base):
    __tablename__ = 'product'
    
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    category_name: Mapped[str] = mapped_column(String, ForeignKey('categories.name'), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    category = relationship("CategoryModel", back_populates="products")

    def __init__(self, product: Product):
        self.name = product.name
        self.description = product.description
        self.category_name = product.category.name
        self.price = product.price
        self.quantity = product.quantity
    