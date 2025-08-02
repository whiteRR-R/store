from typing import List
from domain.interfaces import transaction_manager
from domain.interfaces.repositories import brand_repository
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.dtos.brand_dto import BrandDTO
from application.exceptions import DataNotFoundException
from application.factories.brand_factory import BrandFactory


class GetAllBrandUseCase:
    def __init__(
        self,
        brand_repository: BrandRepositoryProtocol,
    ):
        self.brand_repository = brand_repository

    async def execute(self) -> List[BrandDTO]:
        brands = await self.brand_repository.get_all()
        return [BrandFactory.to_dto(brand) for brand in brands]
