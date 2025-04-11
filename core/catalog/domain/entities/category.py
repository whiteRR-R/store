from uuid import uuid4, UUID
from domain.value_objects.catalog_name import CategoryName
from domain.value_objects.description import Description


class Category:
    def __init__(self, name: CategoryName, description: Description):
        self._name = name
        self._description = description
        
    @classmethod
    def create(cls, name: str, description: str):
        name_vo = CategoryName(name)
        description_vo = Description(description)
        
        return cls(
            name=name_vo,
            description=description_vo
        )
    
    def update_name(self, new_name: CategoryName) -> None:
        """Update the name of the category."""
        self._name = new_name
    
    def update_description(self, new_description: Description) -> None:
        """Update the description of the category."""
        self._description = new_description
        
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description

    def __repr__(self):
        return f"Catalog(catalog_id={self.catalog_id}, name={self.name}, description={self.description})"
