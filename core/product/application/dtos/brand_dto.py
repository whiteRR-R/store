from pydantic import BaseModel
from typing import Optional


class BrandDTO(BaseModel):
    id: Optional[str] = None
    name: str


class CreateBrandDTO(BrandDTO):
    ...

