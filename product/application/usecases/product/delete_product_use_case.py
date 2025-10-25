import logging
from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.repositories.redis_repository import RedisCacheRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class DeleteProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        cache_repository: RedisCacheRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol,
    ) -> None:
        self.product_repository = product_repository
        self.cache_repository = cache_repository
        self.transaction_manager = transaction_manager

    async def execute(self, product_id: UUID) -> None:
        logger.info("Starting deletion of product with ID %s", product_id)
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            logger.warning("Product with ID %s does not exist.", product_id)
            raise DataNotFoundException(f"Product with ID {product_id} does not exist.")
        
        cache_key = "products:{product_id}"
        await self.cache_repository.delete(cache_key)
        logger.info("Deleting product with ID %s from cache", product_id)
        await self.product_repository.delete(product)
        logger.info("Deleted product with ID %s. Committing ...", product_id)
        await self.transaction_manager.commit()
        logger.info("Transaction committed successfully for product %s", product_id)
