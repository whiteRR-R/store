from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from application.exceptions import DataNotFoundException
from uuid import UUID


class DeleteProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
    ):
        self.product_repository = product_repository

    async def execute(self, product_id: UUID) -> None:
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            raise DataNotFoundException(f"Product with IDS {product_id} not found")
        await self.product_repository.delete(product)
    
