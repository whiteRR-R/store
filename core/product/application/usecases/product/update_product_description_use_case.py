from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.value_objects.product_description import ProductDescription
from application.exceptions import DataNotFoundException


class UpdateProductDescriptionUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol) -> None:
        self.product_repository = product_repository
        
    async def execute(self, product_id: UUID, description: str) -> None:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise DataNotFoundException(f"Product with ID {product_id} not found.")
        updated_description = ProductDescription(description)
        product.update_description(updated_description)
        await self.product_repository.update(product)
        
