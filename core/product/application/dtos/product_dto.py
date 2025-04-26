from pydantic import BaseModel
from uuid import UUID
from typing import List


class AttributeDTO(BaseModel):
    name: str
    value: str


class CreateProductDTO(BaseModel):
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO]


class UpdateProductDTO(BaseModel):
    name: str
    description: str
    price: int

