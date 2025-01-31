from domain.interface.uow.base_uow import BaseUnitOfWork
from infrastructure.repository.sqlalchemy_auth_repository import SqlAlchemyAuthRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    """Реализация Unit of Work для SQLAlchemy."""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.new_objects = []
        self.dirty_objects = []
        self.deleted_objects = []
        self._repository = SqlAlchemyAuthRepository(self.session)
    
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
                self._repository.create(object)
            for object in self.deleted_objects:
                self.session.delete(object)
            for object in self.dirty_objects:
                self._repository.update(object)
            await self.session.commit()
            await self.clear()
        except Exception:
            await self.rollback()
    
    async def rollback(self):
        """Откатывает текущую транзакцию."""
        await self.session.rollback()

    async def clear(self):
        self.new_objects.clear()
        self.dirty_objects.clear()
        self.deleted_objects.clear()

    @property
    def repository(self):
        self._repository = SqlAlchemyAuthRepository(self.session)
        return self._repository