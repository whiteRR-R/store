import logging
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from application.dtos.attribute_dto import AttributeDTO

logger = logging.getLogger(__name__)

class CreateAttributeUseCase:
    def __init__(
        self,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol,
    ):
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager

    async def execute(self, attribute_dto: AttributeDTO) -> AttributeDTO:
        logger.info("Start creating attribute with key %s", attribute_dto.key)
        await self.attribute_repository.add(attribute_dto.key)
        logger.info("Attribute with key %s added to repository", attribute_dto.key)
        await self.transaction_manager.commit()
        logger.info("Transaction committed")
        return attribute_dto
