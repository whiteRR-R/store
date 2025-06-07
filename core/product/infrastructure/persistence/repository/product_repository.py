from domain.aggregates.product import ProductRoot
from infrastructure.persistence.models.category_model import CategoryModel
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.datamappers.product_mapper import ProductDataMapper
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Iterable, Optional, AsyncContextManager
from uuid import UUID


class ProductRepository:
    def __init__(self, session_context_manager: AsyncContextManager[AsyncSession]) -> None:
        self.session_context_manager = session_context_manager
        self.mapper = ProductDataMapper()
    
    async def add(
        self,
        product: ProductRoot,
        brand: BrandModel,
        categories: Iterable[CategoryModel]
    ) -> None:
        async with self.session_context_manager as session:
            product_model = self.mapper.entity_to_model(product, brand, categories)
            session.add(product_model)
            await session.commit()
    
    async def delete(self, product: ProductModel) -> None:
        async with self.session_context_manager as session:
            await session.delete(product)
            await session.commit()
    
    async def get_by_id(self, product_id: UUID) -> Optional[ProductRoot]:
        async with self.session_context_manager as session:
            stmt = await session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product = stmt.scalars().one_or_none()
            return self.mapper.model_to_entity(product) if product else None
    
    async def get_all(self) -> List[ProductRoot]:
        async with self.session_context_manager as session:
            stmt = await session.execute(select(ProductModel))
            products = stmt.scalars().all()
            return [self.mapper.model_to_entity(product) for product in products]
