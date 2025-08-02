from typing import List
from application.dtos.filter_dto import ProductFilterDTO
from application.exceptions import DataNotFoundException
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from application.factories.product_factory import ProductFactory
from application.dtos.product_dto import ProductDTO


class GetAllProductUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository
        
    async def execute(self, filters: ProductFilterDTO) -> List[ProductDTO]:
        products = await self.product_repository.get_all(filters)
        return [ProductFactory.to_dto(product) for product in products]
