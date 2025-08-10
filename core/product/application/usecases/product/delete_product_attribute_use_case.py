import logging
from uuid import UUID
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_attribute import ProductAttribute
from application.dtos.product_dto import AttributeDTO
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class DeleteProductAttributeUseCase:
    def __init__(
        self, 
        product_repository: ProductRepositoryProtocol,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ) -> None:
        self.product_repository = product_repository
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager

    async def execute(self, product_id: UUID, attribute_id: UUID) -> None:
        """
        Deletes a product attribute by its ID.
        """
        logger.info("Starting deletion of attribute %s for product %s", attribute_id, product_id)
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            logger.warning("Product with ID %s does not exist.", product_id)
            raise DataNotFoundException(f"Product with ID {product_id} does not exist.")
        
        attribute = await self.attribute_repository.retrieve_attribute_value(product_id=product_id, attribute_id=attribute_id)
        
        if not attribute:
            logger.warning("Attribute with ID %s does not exist.", attribute_id)
            raise DataNotFoundException(f"Attribute with ID {attribute_id} does not exist.")

        logger.info("Deleting attribute %s from product %s", attribute_id, product_id)
        attribute_vo = ProductAttribute(attribute_id=attribute_id, value=attribute.value)
        product.remove_attribute(attribute_vo)
        
        await self.product_repository.update(product)
        logger.info("Attribute %s deleted successfully from product %s. Committing ...", attribute_id, product_id)
        await self.transaction_manager.commit()
        logger.info("Transaction committed successfully for product %s", product_id)
