from uuid import UUID
from typing import List
from domain.interfaces import transaction_manager
from domain.interfaces.repositories import product_repository
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_image import ProductImage
from application.dtos.product_dto import ImageDTO
from application.exceptions import DataNotFoundException



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
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            raise DataNotFoundException(f"Product with {product_id} not found")
        for image in images:
            image_url = await self.s3_storage.upload(image.file, image.filename)
            image_vo = ProductImage(image_url)
            product.add_image(image_vo)
        
        await self.product_repository.update(product)
        await self.transaction_manager.commit()
        
