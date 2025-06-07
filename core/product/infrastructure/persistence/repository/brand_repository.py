from domain.entities.brand import Brand
from infrastructure.persistence.datamappers.brand_mapper import BrandDataMapper
from infrastructure.persistence.models.brand_model import BrandModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional, AsyncContextManager
from uuid import UUID


class BrandRepository:
    def __init__(self, session_context_manager: AsyncContextManager[AsyncSession]) -> None:
        self.session_context_manager = session_context_manager 
        self.mapper = BrandDataMapper()
        print(f"BrandRepository инициализирован с менеджером контекста сессии: {self.session_context_manager}")

    async def add(self, brand: Brand) -> None:
        async with self.session_context_manager as session: # Получаем актуальную сессию
            brand_model = self.mapper.entity_to_model(brand)
            session.add(brand_model)
            await session.commit()

    async def get_all(self) -> List[Brand]:
        async with self.session_context_manager as session:
            stmt = await session.execute(select(BrandModel))
            brands = stmt.scalars().all()
            return [self.mapper.model_to_entity(brand) for brand in brands]
        
    async def get_by_id(self, brand_id: UUID) -> Optional[Brand]:
        async with self.session_context_manager as session:
            stmt = await session.execute(select(BrandModel).where(BrandModel.id == brand_id))
            brand = stmt.scalars().first()
            if brand:
                return self.mapper.model_to_entity(brand)
            return None
