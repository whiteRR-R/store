from typing import Iterable
from sqlalchemy import UUID, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.attribute_model import AttributeModel


class SQLAlchemyAttributeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, key: str):
        attribute = AttributeModel(key)
        self.session.add(attribute)
    
    async def get_by_id(self, id: UUID):
        stmt = await self.session.execute(select(AttributeModel).where(AttributeModel.id == id))
        attribute = stmt.scalar_one_or_none()
        return attribute
    
    async def get_by_ids(self, ids: Iterable[UUID]):
        stmt = await self.session.execute(select(AttributeModel).where(AttributeModel.id.in_(ids)))
        attributes = stmt.scalars().all()
        return attributes
    
    async def delete(self, id: UUID):
        await self.session.execute(delete(AttributeModel).where(AttributeModel.id == id))
