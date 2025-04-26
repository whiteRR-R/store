from domain.entities.category import Category
from infrastructure.persistence.datamappers.category_mapper import CategoryDataMapper
from infrastructure.persistence.models.category_model import CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable, List, Optional
from sqlalchemy import select
from uuid import UUID


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = CategoryDataMapper()

    async def create(self, category: Category) -> None:
        category_model = self.mapper.entity_to_model(category)
        self.session.add(category_model)
        await self.session.commit()

    async def get_all(self) -> List[Category]:
        stmt = await self.session.execute(select(CategoryModel))
        categories = stmt.scalars().all()
        return [self.mapper.model_to_entity(category) for category in categories]

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        stmt = await self.session.execute(select(CategoryModel).where(CategoryModel.id == category_id))
        category = stmt.scalars().first()
        if category:
            return self.mapper.model_to_entity(category)
        return None

    async def get_by_ids(self, category_ids: Iterable[UUID]) -> List[Category]:
        stmt = await self.session.execute(select(CategoryModel).where(CategoryModel.id.in_(category_ids)))
        categories = stmt.scalars().all()
        return [self.mapper.model_to_entity(category) for category in categories]
