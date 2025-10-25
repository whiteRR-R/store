import logging
from uuid import UUID
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class DeleteBrandUseCase:
    def __init__(
        self,
        brand_repository: BrandRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.brand_repository = brand_repository
        self.transaction_manager = transaction_manager

    async def execute(self, brand_id: UUID) -> UUID:
        logger.info("Starting deletion of brand with id: %s", brand_id)
        brand = await self.brand_repository.get_by_id(brand_id)
        if not brand:
            logger.warning("Brand with id: %s not found", brand_id)
            raise DataNotFoundException(f"Brand with ID {brand_id} not found")
        await self.brand_repository.delete(brand)
        logger.info("Brand with id %s deleted successfully. Committing transaction.", brand_id)
        await self.transaction_manager.commit()
        logger.info("Transaction completed for deleting brand with id: %s", brand_id)
        return brand_id
