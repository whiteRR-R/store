import logging
from domain.entities.brand import Brand
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from application.dtos.brand_dto import CreateBrandDTO
from application.factories.brand_factory import BrandFactory


logger = logging.getLogger(__name__)


class CreateBrandUseCase:
    def __init__(
        self,
        brand_repository: BrandRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.brand_repository = brand_repository
        self.transaction_manager = transaction_manager

    async def execute(self, brand_dto: CreateBrandDTO) -> Brand:
        logger.info("Starting creation of brand with name: %s", brand_dto.name)
        brand = BrandFactory.from_dto(brand_dto)
        await self.brand_repository.add(brand)
        logger.info("Brand with id %s created successfully. Committing transaction", brand.id)
        await self.transaction_manager.commit()
        logger.info("Transaction completed for creating brand with id: %s", brand.id)
        return brand
