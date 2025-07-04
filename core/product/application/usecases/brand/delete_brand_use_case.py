from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from application.exceptions import DataNotFoundException
from uuid import UUID


class DeleteBrandUseCase:
    def __init__(self, brand_repository: BrandRepositoryProtocol):
        self.brand_repository = brand_repository

    async def execute(self, brand_id: UUID) -> None:
        brand = await self.brand_repository.get_by_id(brand_id)
        if not brand:
            raise DataNotFoundException(f"Brand with ID {brand_id} not found")
        await self.brand_repository.delete(brand)
