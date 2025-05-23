from uuid import UUID
from application.exceptions import DataNotFoundException


class DeleteBrandUseCase:
    def __init__(self, brand_repository):
        self.brand_repository = brand_repository

    async def execute(self, brand_id: UUID) -> None:
        brand = await self.brand_repository.get_by_id(brand_id)

        if not brand:
            raise DataNotFoundException(f"Brand with ID {brand_id} not found")
        await self.brand_repository.delete(brand)
