from pydantic import BaseModel, Field
from enum import Enum


class SortField(Enum):
    NAME = "name"
    PRICE = "price"


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class ProductFilterDTO(BaseModel):
    min_price: int | None = Field(None, ge=0)
    max_price: int | None = Field(None, ge=0)
    page: int = Field(1, ge=1)
    _limit: int = 20
    sort_by: SortField = Field(SortField.PRICE)
    order: SortOrder = Field(SortOrder.DESC)

    @property
    def offset(self):
        return (self.page - 1) * self._limit
    
    @property
    def limit(self):
        return self._limit
