from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.dtos.brand_dto import CreateBrandDTO
from application.factories.brand_factory import BrandFactory


class CreateBrandUseCase:
    def __init__(
        self,
        brand_repository: BrandRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.brand_repository = brand_repository
        self.transaction_manager = transaction_manager

    async def execute(self, brand_dto: CreateBrandDTO) -> None:
        brand = BrandFactory.from_dto(brand_dto)
        await self.brand_repository.add(brand)
        await self.transaction_manager.commit()
        return brand.id
