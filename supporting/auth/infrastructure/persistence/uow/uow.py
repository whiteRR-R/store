from typing import Any, Dict, Type, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.exceptions import UnitOfWorkException


class UnitOfWork:
    """Реализация Unit of Work для SQLAlchemy."""
    def __init__(self, session_factory: AsyncContextManager[AsyncSession], mappers_classes: Dict[Type[Any], Type[Any]]):
        self._session_factory = session_factory
        self._mappers_classes = mappers_classes
        self.session: AsyncSession | None = None
        self.new_objects = []
        self.dirty_objects = []
        self.deleted_objects = []
    
    async def __aenter__(self):
        """Вход в контекст Unit of Work."""
        async with self._session_factory() as session:
            self.session = session
            self.mappers = {
                entity: mapper(session)
                for entity, mapper in self._mappers_classes.items()
            }
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        """Выход из контекста Unit of Work."""
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.clear()
        
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
