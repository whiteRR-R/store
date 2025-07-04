from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.value_objects.product_attribute import ProductAttribute
from application.dtos.product_dto import AttributeDTO
from application.exceptions import DataNotFoundException


class DeleteProductAttributeUseCase:
    def __init__(self, product_repository: ProductRepositoryProtocol) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: UUID, attribute_dto: AttributeDTO) -> None:
        """
        Deletes a product attribute by its ID.
        """
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise DataNotFoundException(f"Product with ID {product_id} does not exist.")
        
        attribute = ProductAttribute(key=attribute_dto.key, value=attribute_dto.value)
        product.remove_attribute(attribute)
        await self.product_repository.update(product)
