from domain.entities.category import Category
from infrastructure.persistence.datamappers.category_mapper import CategoryDataMapper
from infrastructure.persistence.models.category_model import CategoryModel
from infrastructure.persistence.decorators import transaction
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, List, Optional, AsyncContextManager
from sqlalchemy import select
from uuid import UUID


class CategoryRepository:
    def __init__(self, session_context_manager: AsyncContextManager[AsyncSession]) -> None:
        self.session_context_manager = session_context_manager
        self.mapper = CategoryDataMapper()

    @transaction
    async def add(self, session: AsyncSession, category: Category) -> None:
        category_model = self.mapper.entity_to_model(category)
        session.add(category_model)
        await session.commit()

    @transaction
    async def get_all(self, session: AsyncSession) -> List[Category]:
        stmt = await session.execute(select(CategoryModel))
        categories = stmt.scalars().all()
        return [self.mapper.model_to_entity(category) for category in categories]

    @transaction
    async def get_by_id(self, session: AsyncSession, category_id: UUID) -> Optional[Category]:
        stmt = await session.execute(select(CategoryModel).where(CategoryModel.id == category_id))
        category = stmt.scalars().first()
        if category:
            return self.mapper.model_to_entity(category)
        return None

    @transaction
    async def get_by_ids(self, session: AsyncSession, category_ids: Iterable[UUID]) -> List[Category]:
        stmt = await session.execute(select(CategoryModel).where(CategoryModel.id.in_(category_ids)))
        categories = stmt.scalars().all()
        return [self.mapper.model_to_entity(category) for category in categories]
