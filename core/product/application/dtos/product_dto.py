from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class AttributeDTO(BaseModel):
    name: str
    value: str


class ProductDTO(BaseModel):
    id: Optional[str] = None
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO]

class CreateProductDTO(ProductDTO):
    ...
