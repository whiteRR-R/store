from domain.entities.category import Category
from typing import Protocol


class CategoryRepositoryProtocol(Protocol):
    async def add(self, category: Category):
        """Add a new category to the repository."""
        pass
    
    async def get_by_name(self, name: str) -> Category | None:
        """Retrieve a category by its name."""
        pass
    
    async def get_all(self) -> list[Category]:
        """Retrieve all categories from the repository."""
        pass
