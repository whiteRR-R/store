from domain.aggregates.product import ProductRoot
from infrastructure.persistence.models.category_model import CategoryModel
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.datamappers.product_mapper import ProductDataMapper
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Iterable, Optional
from uuid import UUID


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = ProductDataMapper()
    
    async def create(
        self,
        product: ProductRoot,
        brand: BrandModel,
        categories: Iterable[CategoryModel]
    ) -> None:
        
        product_model = self.mapper.entity_to_model(product, brand, categories)
        self.session.add(product_model)
        await self.session.commit()
    
    async def delete(self, product: ProductModel) -> None:
        await self.session.delete(product)
        await self.session.commit()
    
    async def get_by_id(self, product_id: UUID) -> Optional[ProductRoot]:
        stmt = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = stmt.scalars().one_or_none()
        return self.mapper.model_to_entity(product) if product else None
    
    async def get_all(self) -> List[ProductRoot]:
        stmt = await self.session.execute(select(ProductModel))
        products = stmt.scalars().all()
        return [self.mapper.model_to_entity(product) for product in products]
