from uuid import UUID
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.exceptions import DataNotFoundException


class DeleteBrandUseCase:
    def __init__(
        self,
        brand_repository: BrandRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.brand_repository = brand_repository
        self.transaction_manager = transaction_manager

    async def execute(self, brand_id: UUID) -> None:
        brand = await self.brand_repository.get_by_id(brand_id)
        if not brand:
            raise DataNotFoundException(f"Brand with ID {brand_id} not found")
        await self.brand_repository.delete(brand)
        await self.transaction_manager.commit()
