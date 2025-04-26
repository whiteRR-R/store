from domain.interfaces.product_repository import ProductRepositoryProtocol
from domain.interfaces.category_repository import CategoryRepositoryProtocol
from domain.interfaces.brand_repository import BrandRepositoryProtocol
from application.exceptions import DataNotFoundException 
from application.factories.product_factory import ProductFactory
from application.dtos.product_dto import CreateProductDTO


class CreateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        category_repository: CategoryRepositoryProtocol,
        brand_repository: BrandRepositoryProtocol,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.brand_repository = brand_repository
   
    async def execute(self, product_dto: CreateProductDTO) -> None:
        """
        Creates a new product.
        """
        
        brand = await self.brand_repository.get_by_id(product_dto.brand_id)
        category_ids = tuple(category_id for category_id in product_dto.category_ids)
        categories = await self.category_repository.get_by_ids(category_ids)
        if not brand or not categories:
            raise DataNotFoundException("Brand or Categories not found")
        product = ProductFactory.create_from_dto(product_dto, brand, categories)
        await self.product_repository.create(product)

