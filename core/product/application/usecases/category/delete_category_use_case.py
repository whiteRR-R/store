from uuid import UUID
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.exceptions import DataNotFoundException



class DeleteCategoryUseCase:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol,
    ):
        self.category_repository = category_repository
        self.transaction_manager = transaction_manager
    
    async def execute(self, category_id: UUID) -> UUID:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise DataNotFoundException(f"Category with {category_id} IDS not found")
        await self.category_repository.delete(category)
        await self.transaction_manager.commit()
        return category_id
