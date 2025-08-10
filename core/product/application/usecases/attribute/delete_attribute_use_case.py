import logging
from uuid import UUID
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


class DeleteAttributeUseCase:
    def __init__(
        self,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ) -> None:
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager
    
    async def execute(self, attribute_id: UUID) -> UUID:
        logger.info("Starting deletion of attribute with id: %s", attribute_id)
        attribute = await self.attribute_repository.get_by_id(attribute_id)
        
        if not attribute:
            logger.warning("Attribute with id %s not found", attribute_id)
            raise DataNotFoundException("Attribute with id %s not found", attribute_id)

        logger.info("Attribute with id %s found. Deleting...", attribute_id)
        await self.attribute_repository.delete(attribute_id)
        logger.info("Attribute with id %s deleted successfully. Committing transaction.", attribute_id)
        await self.transaction_manager.commit()
        logger.info("Transaction completed for deleting attribute with id %s", attribute_id)
        return attribute_id
