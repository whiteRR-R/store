import json
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from application.factories.product_factory import ProductFactory
from domain.aggregates.product import ProductRoot
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.repositories.redis_repository import RedisCacheRepositoryProtocol
from application.exceptions import DataNotFoundException
from application.dtos.product_dto import ProductDTO


class GetByIdProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepositoryProtocol,
        cache_repository: RedisCacheRepositoryProtocol,
    ) -> None:
        self.product_repository = product_repository
        self.cache_repository = cache_repository
        
    async def execute(self, product_id: UUID) -> ProductDTO:
        cache_key = f"products:{product_id}"
        cached_data = await self.cache_repository.get_by_key(cache_key)
        
        if cached_data:
            return ProductDTO(**json.loads(cached_data.decode('utf-8')))
        
        product = await self.product_repository.get_by_id(product_id)
    
        if not product:
            raise DataNotFoundException(f"Product with {product_id} IDS not found")
        
        product_dto = ProductFactory.to_dto(product)
        await self.cache_repository.set(cache_key, product_dto.model_dump_json())
        
        return product_dto

