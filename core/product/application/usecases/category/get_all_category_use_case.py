from domain.entities.category import Category
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.factories.category_factory import CategoryFactory
from application.exceptions import DataNotFoundException
from application.dtos.category_dto import CategoryDTO
from typing import List


class GetAllCategoryUseCase:
    def __init__(self, category_repository: CategoryRepositoryProtocol):
        self.category_repository = category_repository
    
    async def execute(self) -> List[CategoryDTO]:
        categories = await self.category_repository.get_all()
        return [CategoryFactory.to_dto(category) for category in categories]
