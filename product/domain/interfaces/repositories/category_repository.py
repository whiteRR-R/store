from domain.entities.category import Category
from typing import Iterable, Protocol, List
from uuid import UUID


class CategoryRepositoryProtocol(Protocol):
    async def add(self, category: Category) -> None:
        """
        Adds a new category to the repository.
        """
        ...
    
    async def delete(self, category: Category) -> None:
        """
        Delete category by id
        """
        ...
    
    async def get_all(self) -> List[Category]:
        """
        Retrieves all categories from the repository.
        """
        ...
    
    async def get_by_id(self, category_id: UUID) -> Category:
        """
        Gets a category by its ID.
        """
        ...
    
    async def get_by_ids(self, category_ids: Iterable[UUID]) -> List[Category]:
        """
        Gets categories by their IDs.
        """
        ...
