from pydantic import BaseModel, Field
from enum import Enum


class SortField(Enum):
    name = "name"
    price = "price"


class SortOrder(Enum):
    asc = "asc"
    desc = "desc"


class ProductFilterDTO(BaseModel):
    min_price: int | None = Field(None, ge=0)
    max_price: int | None = Field(None, ge=0)
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    sort_by: SortField = Field(SortField.price)
    order: SortOrder = Field(SortOrder.desc)
