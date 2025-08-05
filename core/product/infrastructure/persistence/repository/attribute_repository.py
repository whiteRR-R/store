import uuid
from typing import Iterable
from sqlalchemy import UUID, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.attribute_model import AttributeModel
from infrastructure.persistence.models.association_models import AssosiationProductAttributeModel


class SQLAlchemyAttributeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, key: str):
        attribute = AttributeModel(id=uuid.uuid4(), name=key)
        self.session.add(attribute)
    
    async def get_by_id(self, attribute_id: UUID):
        stmt = await self.session.execute(select(AttributeModel).where(AttributeModel.id == attribute_id))
        attribute = stmt.scalar_one_or_none()
        return attribute
    
    async def get_by_ids(self, ids: Iterable[UUID]):
        stmt = await self.session.execute(select(AttributeModel).where(AttributeModel.id.in_(ids)))
        attributes = stmt.scalars().all()
        return attributes

    async def get_all(self):
        stmt = await self.session.execute(select(AttributeModel))
        attributes = stmt.scalars().all()
        return attributes
    
    async def retrieve_attribute_value(self, product_id: UUID, attribute_id: UUID):
        stmt = await self.session.execute(
            select(AssosiationProductAttributeModel)
            .where(AssosiationProductAttributeModel.attribute_id == attribute_id)
            .where(AssosiationProductAttributeModel.product_id == product_id)
            )
        attribute = stmt.scalar_one_or_none()
        return attribute
    
    async def delete(self, attribute_id: UUID):
        await self.session.execute(delete(AttributeModel).where(AttributeModel.id == attribute_id))
