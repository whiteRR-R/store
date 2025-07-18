from uuid import UUID
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException


class DeleteProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.product_repository = product_repository
        self.transaction_manager = transaction_manager

    async def execute(self, product_id: UUID) -> None:
        product = await self.product_repository.get_by_id(product_id)
        
        if not product:
            raise DataNotFoundException(f"Product with IDS {product_id} not found")
        
        await self.product_repository.delete(product)
        await self.transaction_manager.commit()
    
