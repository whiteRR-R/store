from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class BrandDTO(BaseModel):
    id: UUID
    name: str


class CreateBrandDTO(BaseModel):
    name: str
    
