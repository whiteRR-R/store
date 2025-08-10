import logging
from uuid import UUID
from domain.entities.category import Category
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.dtos.category_dto import CreateCategoryDTO
from application.factories.category_factory import CategoryFactory
from application.exceptions import ApplicationException
from domain.interfaces.transaction_manager import TransactionManagerProcotol

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.category_repository = category_repository
        self.transaction_manager = transaction_manager

    async def execute(self, category_dto: CreateCategoryDTO) -> Category:
        try:
            logger.info("Creating category with name: %s", category_dto.name)
            category = CategoryFactory.from_dto(category_dto)
            await self.category_repository.add(category)
            logger.info("Category created successfully: %s. Committing transaction ...", category.name)
            await self.transaction_manager.commit()
            logger.info("Transaction completed for category with id: %s", category.id)
            return category
        except ApplicationException:
            logger.error("Category %s not created", category_dto.name)
            await self.transaction_manager.rollback()
            raise ApplicationException(f"Сategory {category_dto.name} not created")
