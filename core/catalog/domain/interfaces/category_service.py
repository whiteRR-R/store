from typing import Protocol
from domain.entities.category import Category

class CategoryServiceProtocol(Protocol):
    async def add_category(self, name: str) -> None:
        """Add a new category."""
        pass

    async def get_all_categories(self) -> list[Category]:
        """Retrieve all categories."""
        pass
