from domain.aggregates.product import ProductRoot
from infrastructure.persistence.models.category_model import CategoryModel
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.datamappers.product_mapper import ProductDataMapper
from infrastructure.persistence.decorators import transaction
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Iterable, Optional, AsyncContextManager
from uuid import UUID


class ProductRepository:
    def __init__(self, session_context_manager: AsyncContextManager[AsyncSession]) -> None:
        self.session_context_manager = session_context_manager
        self.mapper = ProductDataMapper()
    
    @transaction
    async def add(
        self,
        session: AsyncSession,
        product: ProductRoot,
        brand: BrandModel,
        categories: Iterable[CategoryModel]
    ) -> None:
        product_model = self.mapper.entity_to_model(product, brand, categories)
        session.add(product_model)
        await session.commit()
    
    @transaction
    async def delete(self, session: AsyncSession, product: ProductModel) -> None:
        await session.delete(product)
        await session.commit()
    
    @transaction
    async def get_by_id(self, session: AsyncSession, product_id: UUID) -> Optional[ProductRoot]:
        stmt = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = stmt.scalars().one_or_none()
        return self.mapper.model_to_entity(product) if product else None
    
    @transaction
    async def get_all(self, session: AsyncSession) -> List[ProductRoot]:
        stmt = await session.execute(select(ProductModel))
        products = stmt.scalars().all()
        return [self.mapper.model_to_entity(product) for product in products]
