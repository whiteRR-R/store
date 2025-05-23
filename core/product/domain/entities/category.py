from domain.value_objects.category_name import CategoryName
from typing import Optional
from uuid import uuid4, UUID


class Category:
    def __init__(self, category_name: CategoryName, id: Optional[UUID] = None):
        self._id = id or uuid4()
        self._name = category_name

    def update_name(self, new_name: CategoryName) -> None:
        self._name = new_name
    
    @property
    def name(self) -> CategoryName:
        return self._name
    
    @property
    def id(self) -> UUID:
        return self._id
    
    def __repr__(self):
        return f"Category(id={self._id}, name={self._name})"
