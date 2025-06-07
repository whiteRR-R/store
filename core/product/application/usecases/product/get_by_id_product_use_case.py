from application.factories.product_factory import ProductFactory
from domain.aggregates.product import ProductRoot
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from application.exceptions import DataNotFoundException
from application.dtos.product_dto import ProductDTO
from uuid import UUID


class GetByIdProductUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository
        
    async def execute(self, product_id: UUID) -> ProductDTO:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise DataNotFoundException(f"Product with {product_id} IDS not found")
        return ProductFactory.to_dto(product)
