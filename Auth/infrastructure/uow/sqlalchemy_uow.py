from domain.abstacts.uow.base_uow import BaseUnitOfWork
from infrastructure.uow.sqlalchemy_uow import SqlAlchemyAuthRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    """Реализация Unit of Work для SQLAlchemy."""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.auth_repository = None
    
    async def __aenter__(self):
        """Вход в асинхронный контекст Unit of Work."""
        self.auth_repository = SqlAlchemyAuthRepository(self.session)
        return await super().__aenter__()
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        """Выход из асинхронного контекста Unit of Work."""
        if exc_type is not None:
            await self.rollback()
        await self.session.close()
        await super().__aexit__(exc_type, exc_value, traceback)
    
    async def commit(self):
        """Подтверждает текущую транзакцию."""
        return self.session.commit()
    
    async def flush(self):
        """Сбрасывает изменения в текущую транзакцию."""
        await self.session.flush()
    
    async def rollback(self):
        """Откатывает текущую транзакцию."""
        await self.session.rollback()

