from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.dtos.category_dto import CreateCategoryDTO
from application.factories.category_factory import CategoryFactory


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepositoryProtocol):
        self.category_repository = category_repository
    
    async def execute(self, category_dto: CreateCategoryDTO) -> None:
        category = CategoryFactory.from_dto(category_dto)
        await self.category_repository.add(category)
