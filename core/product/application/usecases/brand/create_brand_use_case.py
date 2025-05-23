from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from application.dtos.brand_dto import CreateBrandDTO
from application.factories.brand_factory import BrandFactory


class CreateBrandUseCase:
    def __init__(self, brand_repository: BrandRepositoryProtocol):
        self.brand_repository = brand_repository

    async def execute(self, brand_dto: CreateBrandDTO) -> None:
        brand = BrandFactory.from_dto(brand_dto)
        await self.brand_repository.create(brand)
        
