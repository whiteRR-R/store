from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.exceptions import DataNotFoundException
from uuid import UUID


class DeleteCategoryUseCase:
    def __init__(self, category_repository: CategoryRepositoryProtocol):
        self.category_repository = category_repository
    
    async def execute(self, category_id: UUID) -> None:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise DataNotFoundException(f"Category with {category_id} IDS not found")
        await self.category_repository.delete(category)
