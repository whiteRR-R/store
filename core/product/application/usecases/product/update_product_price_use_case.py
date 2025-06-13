from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.value_objects.product_price import ProductPrice
from application.exceptions import DataNotFoundException


class UpdateProductPriceUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository
        
    async def execute(self, product_id: UUID, price: int):
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise DataNotFoundException(f"Product with {product_id} not found")
        updated_price = ProductPrice(price)
        product.update_price(updated_price)
        await self.product_repository.update(product)
