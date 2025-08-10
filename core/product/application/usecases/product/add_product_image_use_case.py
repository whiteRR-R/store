import logging
from uuid import UUID
from typing import List
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_image import ProductImage
from application.dtos.product_dto import ImageDTO
from application.exceptions import DataNotFoundException


logger = logging.getLogger(__name__)


class AddProductImageUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        s3_storage: S3ImageStorageProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.product_repository = product_repository
        self.transaction_manager = transaction_manager
        self.s3_storage = s3_storage
        
    async def execute(self, product_id: UUID, images: List[ImageDTO]):
        logger.info("Starting add images to product %s", product_id)
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            logger.warning("Product with id %s not found", product_id)
            raise DataNotFoundException(f"Product with {product_id} not found")
        
        for image in images:
            logger.info("Uploading image %s for product %s", image.filename, product_id)
            image_url = await self.s3_storage.upload(image.file, image.filename)
            logger.info("Image %s uploaded successfully, URL: %s", image.filename, image_url)
            image_vo = ProductImage(image_url)
            product.add_image(image_vo)
        
        await self.product_repository.update(product)
        logger.info("All images added to product %s. Committing transaction ...", product_id)
        await self.transaction_manager.commit()
        logger.info("Transaction committed successfully for product %s", product_id)
