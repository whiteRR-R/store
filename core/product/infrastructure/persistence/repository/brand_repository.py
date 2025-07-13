from domain.entities.brand import Brand
from infrastructure.persistence.datamappers.brand_mapper import BrandDataMapper
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.decorators import transaction
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Callable, AsyncContextManager
from sqlalchemy import select, delete
from uuid import UUID


class BrandRepository:
    def __init__(self, session_context_manager: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self.session_context_manager = session_context_manager
        self.mapper = BrandDataMapper()

    @transaction
    async def add(self, session: AsyncSession, brand: Brand) -> None:
        brand_model = self.mapper.entity_to_model(brand)
        session.add(brand_model)
        await session.commit()
        return brand

    @transaction
    async def get_all(self, session: AsyncSession) -> List[Brand]:        
        stmt = await session.execute(select(BrandModel))
        brands = stmt.scalars().all()
        return [self.mapper.model_to_entity(brand) for brand in brands]
    
    @transaction
    async def get_by_id(self, session: AsyncSession, brand_id: UUID) -> Optional[Brand]:
        stmt = await session.execute(select(BrandModel).where(BrandModel.id == brand_id))
        brand = stmt.scalars().first()
        if brand:
            return self.mapper.model_to_entity(brand)
        return None

    @transaction
    async def delete(self, session: AsyncSession, brand: Brand) -> None:
        brand_model = self.mapper.entity_to_model(brand)
        await session.execute(delete(BrandModel).where(BrandModel.id == brand.id))
        await session.commit()
