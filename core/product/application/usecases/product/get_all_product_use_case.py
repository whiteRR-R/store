from application.exceptions import DataNotFoundException
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from application.factories.product_factory import ProductFactory
from application.dtos.product_dto import ProductDTO
from typing import List


class GetAllProductUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository
        
    async def execute(self) -> List[ProductDTO]:
        products = await self.product_repository.get_all()
        return [ProductFactory.to_dto(product) for product in products]
