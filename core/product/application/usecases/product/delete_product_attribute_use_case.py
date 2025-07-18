from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_attribute import ProductAttribute
from application.dtos.product_dto import AttributeDTO
from application.exceptions import DataNotFoundException


class DeleteProductAttributeUseCase:
    def __init__(
        self, 
        product_repository: ProductRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ) -> None:
        self.product_repository = product_repository
        self.transaction_manager = transaction_manager

    async def execute(self, product_id: UUID, attribute_dto: AttributeDTO) -> None:
        """
        Deletes a product attribute by its ID.
        """
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            raise DataNotFoundException(f"Product with ID {product_id} does not exist.")
        
        attribute = ProductAttribute(attribute_id=attribute_dto.attribute_id, value=attribute_dto.value)
        product.remove_attribute(attribute)
        
        await self.product_repository.update(product)
        await self.transaction_manager.commit()
