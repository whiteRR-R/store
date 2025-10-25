import logging
from uuid import UUID
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_image import ProductImage
from application.dtos.product_dto import DeleteImageDTO
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class DeleteProductImageUseCase:
    
    def __init__(
        self, 
        product_repository: ProductRepositoryProtocol, 
        s3_storage: S3ImageStorageProtocol,
        transaction_manager: TransactionManagerProcotol

    ):
        self.product_repository = product_repository
        self.s3_storage = s3_storage
        self.transaction_manager = transaction_manager
    
    async def execute(self, product_id: UUID, image_url: str) -> None:
        logger.info("Starting deletion of image %s for product %s", image_url, product_id)
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            logger.warning("Product with ID %s does not exist.", product_id)
            raise DataNotFoundException(f"Product with ID {product_id} does not exist.")

        image_vo = ProductImage(image_url)
        product.remove_image(image_vo)
        logger.info("Deleting image %s from product %s", image_url, product_id)
        
        for url in product.images:
            logger.info("Deleting image from S3 storage: %s", url)
            await self.s3_storage.delete(url)
        
        await self.product_repository.update(product)
        logger.info("Image %s deleted successfully from product %s. Committing ...", image_url, product_id)
        await self.transaction_manager.commit()
        logger.info("Transaction committed successfully for product %s", product_id)
