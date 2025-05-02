from domain.entities.category import Category
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from typing import List


class GetAllCategoryUseCase:
    def __init__(self, category_repository: CategoryRepositoryProtocol):
        self.category_repository = category_repository
    
    async def execute(self) -> List[Category]:
        categories = await self.category_repository.get_all()
        return categories
