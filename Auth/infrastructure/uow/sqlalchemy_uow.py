from domain.interface.uow.base_uow import BaseUnitOfWork
from infrastructure.repository.sqlalchemy_auth_repository import SqlAlchemyAuthRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    """Реализация Unit of Work для SQLAlchemy."""
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None
        self._repository = None
    
    async def __aenter__(self):
        """Вход в асинхронный контекст Unit of Work."""
        self.session = self.session_factory()
        return await super().__aenter__()
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        """Выход из асинхронного контекста Unit of Work."""
        if exc_type is not None:
            await self.rollback()
        await self.session.close()
        await super().__aexit__(exc_type, exc_value, traceback)
    
    @property
    async def repository(self):
        self._repository = SqlAlchemyAuthRepository(self.session)
        return self._repository
    
    async def commit(self):
        """Подтверждает текущую транзакцию."""
        return self.session.commit()
    
    async def flush(self):
        """Сбрасывает изменения в текущую транзакцию."""
        await self.session.flush()
    
    async def rollback(self):
        """Откатывает текущую транзакцию."""
        await self.session.rollback()

