from domain.value_objects.brand_name import BrandName 
import uuid


class Brand:
    def __init__(self, brand_name: BrandName):
        self.id = uuid.uuid4()
        self._name = brand_name
        
    def update_name(self, new_name: BrandName) -> None:
        self._name = new_name
        
    @property
    def name(self) -> BrandName:
        return self._name
    
    def __repr__(self):
        return f"Brand(id={self.id}, name={self._name})"
