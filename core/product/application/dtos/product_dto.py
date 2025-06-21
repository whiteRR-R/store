from typing import List, Optional, BinaryIO
from uuid import UUID
from dataclasses import dataclass, field


@dataclass
class AttributeDTO:
    key: str
    value: str

@dataclass
class ImageDTO:
    file: BinaryIO
    filename: str

@dataclass
class DeleteImageDTO:
    url: str

@dataclass
class CreateProductDTO:
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO] = field(default_factory=list)

@dataclass
class ProductDTO:
    id: UUID
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO] = field(default_factory=list)
    images: List[str] = field(default_factory=list)

@dataclass
class UpdateProductDTO(ProductDTO):
    pass
