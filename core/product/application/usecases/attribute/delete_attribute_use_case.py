from uuid import UUID
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException


class DeleteAttributeUseCase:
    def __init__(
        self,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager
    
    async def execute(self, id: UUID):
        attribute = await self.attribute_repository.get_by_id(id)
        
        if attribute:
            raise DataNotFoundException(f"Attribute with {id} not found")
        
        await self.attribute_repository.delete(id)
        await self.transaction_manager.commit()
