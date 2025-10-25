from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class CategoryDTO(BaseModel):
    id: UUID
    name: str


class CreateCategoryDTO(BaseModel):
    name: str
