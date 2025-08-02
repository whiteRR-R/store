from typing import List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from fastapi import UploadFile


class AttributeDTO(BaseModel):
    attribute_id: UUID
    value: str


class DeleteAttributeDTO(BaseModel):
    value: str


class ImageDTO(BaseModel):
    file: UploadFile
    filename: str

    model_config = ConfigDict(arbitrary_types_allowed=True)



class DeleteImageDTO(BaseModel):
    url: str


class CreateProductDTO(BaseModel):
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID] = Field(default_factory=list)
    attributes: List[AttributeDTO] = Field(default_factory=list)


class ProductDTO(BaseModel):
    id: UUID
    name: str
    brand_id: UUID
    description: str
    price: int
    category_ids: List[UUID]
    attributes: List[AttributeDTO] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)


class UpdateProductDTO(ProductDTO):
    pass
