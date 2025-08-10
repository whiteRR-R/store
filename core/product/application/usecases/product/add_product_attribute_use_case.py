import logging
from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_attribute import ProductAttribute
from application.dtos.product_dto import AttributeDTO
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class AddProductAttributeUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.product_repository = product_repository
        self.transaction_manager = transaction_manager

    async def execute(self, product_id: UUID, attribute_dto: AttributeDTO) -> None:
        logger.info("Adding attribute %s to product %s", attribute_dto.attribute_id, product_id)
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            logger.warning("Product with id %s not found", product_id)
            raise DataNotFoundException("Product not found")
        
        attribute = ProductAttribute(attribute_id=attribute_dto.attribute_id,value=attribute_dto.value)
        logger.info("Creating ProductAttribute with id %s and value %s", attribute.attribute_id, attribute.value)
        product.add_attribute(attribute)
        
        await self.product_repository.update(product)
        logger.info("Attribute with id %s added to product %s. Committing ...", attribute_dto.attribute_id, product_id)
        await self.transaction_manager.commit()
        logger.info("Transaction committed successfully for product %s", product_id)
