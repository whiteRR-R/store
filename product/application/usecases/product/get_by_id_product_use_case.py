import json
import logging
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from application.factories.product_factory import ProductFactory
from domain.aggregates.product import ProductRoot
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.repositories.redis_repository import RedisCacheRepositoryProtocol
from application.exceptions import DataNotFoundException
from application.dtos.product_dto import ProductDTO

logger = logging.getLogger(__name__)


class GetByIdProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        cache_repository: RedisCacheRepositoryProtocol,
    ) -> None:
        self.product_repository = product_repository
        self.cache_repository = cache_repository
        
    async def execute(self, product_id: UUID) -> ProductDTO:
        logger.info("Executing GetByIdProductUseCase for product_id: %s", product_id)
        cache_key = "products:%s" % product_id
        cached_data = await self.cache_repository.get_by_key(cache_key)
        
        if cached_data:
            logger.info("Cache hit for key: %s", cache_key)
            return ProductDTO(**json.loads(cached_data.decode('utf-8')))
        
        logger.info("Cache miss for key: %s. Fetching from repository.", cache_key)
        product = await self.product_repository.get_by_id(product_id)
    
        if not product:
            logger.warning("Product with ID %s not found in repository.", product_id)
            raise DataNotFoundException("Product with %s IDS not found" % product_id)
        
        product_dto = ProductFactory.to_dto(product)
        await self.cache_repository.set(cache_key, product_dto.model_dump_json())
        logger.info("Product with ID %s cached under key: %s", product_id, cache_key)
        
        return product_dto
