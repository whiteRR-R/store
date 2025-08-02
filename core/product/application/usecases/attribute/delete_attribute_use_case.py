from uuid import UUID
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException


class DeleteAttributeUseCase:
    def __init__(
        self,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ) -> None:
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager
    
    async def execute(self, attribute_id: UUID) -> UUID:
        attribute = await self.attribute_repository.get_by_id(attribute_id)
        
        if attribute:
            raise DataNotFoundException(f"Attribute with {attribute_id} not found")
        
        await self.attribute_repository.delete(attribute_id)
        await self.transaction_manager.commit()
        return attribute_id
