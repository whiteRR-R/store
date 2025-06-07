from domain.entities.category import Category
from infrastructure.persistence.datamappers.category_mapper import CategoryDataMapper
from infrastructure.persistence.models.category_model import CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, List, Optional, AsyncContextManager
from sqlalchemy import select
from uuid import UUID


class CategoryRepository:
    def __init__(self, session_context_manager: AsyncContextManager[AsyncSession]) -> None:
        self.session_context_manager = session_context_manager
        self.mapper = CategoryDataMapper()

    async def add(self, category: Category) -> None:
        async with self.session_context_manager as session:
            category_model = self.mapper.entity_to_model(category)
            session.add(category_model)
            await session.commit()

    async def get_all(self) -> List[Category]:
        async with self.session_context_manager as session:    
            stmt = await session.execute(select(CategoryModel))
            categories = stmt.scalars().all()
            return [self.mapper.model_to_entity(category) for category in categories]

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        async with self.session_context_manager as session:
            stmt = await session.execute(select(CategoryModel).where(CategoryModel.id == category_id))
            category = stmt.scalars().first()
            if category:
                return self.mapper.model_to_entity(category)
            return None

    async def get_by_ids(self, category_ids: Iterable[UUID]) -> List[Category]:
        async with self.session_context_manager as session:
            stmt = await session.execute(select(CategoryModel).where(CategoryModel.id.in_(category_ids)))
            categories = stmt.scalars().all()
            return [self.mapper.model_to_entity(category) for category in categories]
