from uuid import UUID
from typing import List, Protocol
from application.dtos.category_dto import CreateCategoryDTO, CategoryDTO


class CreateCategoryUseCaseProtocol(Protocol):
    async def execute(self, category_dto: CreateCategoryDTO) -> UUID:
        """Create a new category."""
        pass


class DeleteCategoryUseCaseProtocol(Protocol):
    async def execute(self, category_id: UUID) -> None:
        """Delete a category by its ID."""
        pass
    

class GetAllCategoriesUseCaseProtocol(Protocol):
    async def execute(self) -> List[CategoryDTO]:
        """Retrieve all categories."""
        pass
