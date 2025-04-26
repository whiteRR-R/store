from domain.value_objects.brand_name import BrandName 
from uuid import uuid4, UUID
from typing import Optional


class Brand:
    def __init__(self, brand_name: BrandName, id: Optional[UUID] = None):
        self._id = id or uuid4()
        self._name = brand_name
        
    def update_name(self, new_name: BrandName) -> None:
        self._name = new_name
        
    @property
    def name(self) -> BrandName:
        return self._name
    
    def __repr__(self):
        return f"Brand(id={self._id}, name={self._name})"
