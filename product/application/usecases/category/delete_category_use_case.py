import logging
from uuid import UUID
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol,
    ):
        self.category_repository = category_repository
        self.transaction_manager = transaction_manager
    
    async def execute(self, category_id: UUID) -> UUID:
        logger.info("Starting deletion of category with id: %s", category_id)
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            logger.warning("Category with id %s not found", category_id)
            raise DataNotFoundException("Category with id %s not found", category_id)
        await self.category_repository.delete(category)
        await self.transaction_manager.commit()
        logger.info("Category with id %s deleted successfully", category_id)
        return category_id
