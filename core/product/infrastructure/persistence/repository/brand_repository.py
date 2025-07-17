from domain.entities.brand import Brand
from infrastructure.persistence.datamappers.brand_mapper import BrandDataMapper
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.decorators import transaction
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Callable, AsyncContextManager
from sqlalchemy import select, delete
from uuid import UUID


class SQLAlchemyBrandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = BrandDataMapper()


    async def add(self, brand: Brand) -> None:
        brand_model = self.mapper.entity_to_model(brand)
        self.session.add(brand_model)
        

    async def get_all(self) -> List[Brand]:        
        stmt = await self.session.execute(select(BrandModel))
        brands = stmt.scalars().all()
        return [self.mapper.model_to_entity(brand) for brand in brands]
    

    async def get_by_id(self, brand_id: UUID) -> Optional[Brand]:
        stmt = await self.session.execute(select(BrandModel).where(BrandModel.id == brand_id))
        brand = stmt.scalars().first()
        if brand:
            return self.mapper.model_to_entity(brand)
        return None


    async def delete(self, brand: Brand) -> None:
        await self.session.execute(delete(BrandModel).where(BrandModel.id == brand.id))
