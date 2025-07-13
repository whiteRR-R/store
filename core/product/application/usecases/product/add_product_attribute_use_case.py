from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.value_objects.product_attribute import ProductAttribute
from application.dtos.product_dto import AttributeDTO
from application.exceptions import DataNotFoundException


class AddProductAttributeUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol):
        self.product_repository = product_repository

    async def execute(self, product_id: UUID, attribute_dto: AttributeDTO) -> None:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise DataNotFoundException("Product not found")
        
        attribute = ProductAttribute(
            attribute_id=attribute_dto.attribute_id,
            value=attribute_dto.value
        )
        product.add_attribute(attribute)
        await self.product_repository.update(product)
