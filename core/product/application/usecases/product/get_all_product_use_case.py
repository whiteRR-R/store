from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.aggregates.product import ProductRoot
from typing import List


class GetAllProductUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository
        
    async def execute(self) -> List[ProductRoot]:
        products = await self.product_repository.get_all()
        return products
