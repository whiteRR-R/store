from application.dtos.brand_dto import BrandDTO
from application.exceptions import DataNotFoundException
from application.factories.brand_factory import BrandFactory
from typing import List


class GetAllBrandUseCase:
    def __init__(self, brand_repository):
        self.brand_repository = brand_repository

    async def execute(self) -> List[BrandDTO]:
        brands = await self.brand_repository.get_all()
        if not brands:
            raise DataNotFoundException("No brands found.")
        return [BrandFactory.to_dto(brand) for brand in brands]
