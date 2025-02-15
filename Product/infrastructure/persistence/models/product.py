from decimal import Decimal
from math import prod
from typing import Any
from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.persistence.database import Base
from domain.entities.product import Product


class ProductModel(Base):
    __tablename__ = 'product'
    
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, product: Product):
        self.name = product.name
        self.description = product.description
        self.category = product.category.name
        self.price = product.price
        self.quantity = product.quantity
    