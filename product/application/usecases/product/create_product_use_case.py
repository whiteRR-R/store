import logging
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.value_objects.product_attribute import ProductAttribute
from application.exceptions import DataNotFoundException 
from application.factories.product_factory import ProductFactory
from application.dtos.product_dto import CreateProductDTO


logger = logging.getLogger(__name__)


class CreateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        category_repository: CategoryRepositoryProtocol,
        brand_repository: BrandRepositoryProtocol,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.brand_repository = brand_repository
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager 

    async def execute(self, product_dto: CreateProductDTO) -> None:
        """
        Creates a new product.
        """
        logger.info("Creating product with name %s", product_dto.name)
        category_ids = tuple(category_id for category_id in product_dto.category_ids)
        attribute_ids = tuple(attr.attribute_id for attr in product_dto.attributes)
        brand = await self.brand_repository.get_by_id(product_dto.brand_id)
        categories = await self.category_repository.get_by_ids(category_ids)
        attributes = await self.attribute_repository.get_by_ids(attribute_ids)
        
        if not brand:
            logger.warning("Brand with id %s not found", product_dto.brand_id)
            raise DataNotFoundException(f"Brand: {product_dto.brand_id} not found")
        if len(categories) != len(category_ids):
            logger.warning("Categories not found or not equal count")
            raise DataNotFoundException("Categories not found or not equal count")
        if len(attributes) != len(attribute_ids):
            logger.warning("Attributes not found or not equal count")
            raise DataNotFoundException("Attributes not found or not equal count")
        
        product = ProductFactory.from_dto(product_dto, brand, categories)
        logger.info("Product created successfully with id %s. Committing ...", product.id)
        await self.product_repository.add(product)
        await self.transaction_manager.commit()
        logger.info("Transaction committed successfully for product %s", product.id)
