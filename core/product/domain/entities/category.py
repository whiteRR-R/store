from domain.value_objects.category_name import CategoryName
import uuid


class Category:
    def __init__(self, category_name: CategoryName):
        self.id = uuid.uuid4()
        self._name = category_name

    def update_name(self, new_name: CategoryName) -> None:
        self._name = new_name
    
    @property
    def name(self) -> CategoryName:
        return self._name
    
    def __repr__(self):
        return f"Category(id={self.id}, name={self._name})"
