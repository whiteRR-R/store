from uuid import UUID
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.value_objects.product_image import ProductImage
from application.interfaces.usecases.product_use_cases import DeleteProductImageUseCaseProtocol
from application.dtos.product_dto import DeleteImageDTO
from application.exceptions import DataNotFoundException


class DeleteProductImageUseCase(DeleteProductImageUseCaseProtocol):
    
    def __init__(self, product_repository: ProductRepositoryProtocol, s3_storage: S3ImageStorageProtocol):
        self.product_repository = product_repository
        self.s3_storage = s3_storage
    
    async def execute(self, product_id: UUID, image: DeleteImageDTO) -> None:
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            raise DataNotFoundException(f"Product with {product_id} not found")
        image_vo = ProductImage(image.url)
        product.remove_image(image_vo)
        
        for url in product.images:
            await self.s3_storage.delete(url)
        
        await self.product_repository.update(product)
