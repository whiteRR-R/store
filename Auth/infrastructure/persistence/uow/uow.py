from infrastructure.exceptions import UnitOfWorkException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Type


class UnitOfWork:
    """Реализация Unit of Work для SQLAlchemy."""
    def __init__(self, session: AsyncSession, mappers: Dict[Type, Any]):
        self.session = session
        self.mappers = mappers
        self.new_objects = []
        self.dirty_objects = []
        self.deleted_objects = []
    
    async def register_new(self, obj):
        self.new_objects.append(obj)
    
    async def register_dirty(self, obj):
        self.dirty_objects.append(obj)
    
    async def register_deleted(self, obj):
        self.deleted_objects.append(obj)
    
    async def commit(self):
        """Подтверждает текущую транзакцию."""
        try:
            for object in self.new_objects:
                await self.mappers[type(object)].add(object)
            for object in self.deleted_objects:
                await self.mappers[type(object)].delete(object)
            for object in self.dirty_objects:
                await self.mappers[type(object)].update(object)
            await self.session.commit()
            await self.clear()
        except Exception as exception:
            await self.rollback()
            raise UnitOfWorkException(f"Failed to commit: {str(exception)}")

    async def rollback(self):
        """Откатывает текущую транзакцию."""
        await self.session.rollback()

    async def clear(self):
        """Очищает списки объектов."""
        self.new_objects.clear()
        self.dirty_objects.clear()
        self.deleted_objects.clear()
