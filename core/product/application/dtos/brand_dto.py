import uuid
from pydantic import BaseModel
from typing import Optional


class BrandDTO(BaseModel):
    id: uuid.UUID
    name: str


class CreateBrandDTO(BaseModel):
    name: str
    
