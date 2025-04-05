from domain.entities.category import Category
from typing import Protocol


class CategoryRepositoryProtocol(Protocol):
    def add(self, category: Category):
        """Add a new category to the repository."""
        pass
    
    def get_all(self) -> list[Category]:
        """Retrieve all categories from the repository."""
        pass
