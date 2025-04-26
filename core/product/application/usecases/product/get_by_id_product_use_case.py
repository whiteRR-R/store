from domain.aggregates.product import ProductRoot
from domain.interfaces.product_repository import ProductRepositoryProtocol
from application.exceptions import DataNotFoundException
from uuid import UUID


class GetByIdProductUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository
        
    async def execute(self, product_id: UUID) -> ProductRoot:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise DataNotFoundException(f"Product with {product_id} IDS not found")
        return product
