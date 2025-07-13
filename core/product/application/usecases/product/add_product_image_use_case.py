from uuid import UUID
from typing import List
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from domain.value_objects.product_image import ProductImage
from application.dtos.product_dto import ImageDTO
from application.exceptions import DataNotFoundException



class AddProductImageUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol, s3_storage: S3ImageStorageProtocol):
        self.product_repository = product_repository
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
