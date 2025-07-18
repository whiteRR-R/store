from uuid import UUID
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.dtos.category_dto import CreateCategoryDTO
from application.factories.category_factory import CategoryFactory
from application.exceptions import ApplicationException
from domain.interfaces.transaction_manager import TransactionManagerProcotol


class CreateCategoryUseCase:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol

    ):
        self.category_repository = category_repository
        self.transaction_manager = transaction_manager

    async def execute(self, category_dto: CreateCategoryDTO) -> UUID:
        try:
            category = CategoryFactory.from_dto(category_dto)            
            await self.category_repository.add(category)
            await self.transaction_manager.commit()
            return category.id
        except ApplicationException:
            raise ApplicationException(f"Сategory {category.name} not created")
            

