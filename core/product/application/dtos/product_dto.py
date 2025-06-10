from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class AttributeDTO(BaseModel):
    key: str
    value: str


class CreateProductDTO(BaseModel):
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO]


class ProductDTO(CreateProductDTO):
    id: UUID
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO]


class UpdateProductDTO(ProductDTO):
    ...
