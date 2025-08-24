from typing import AsyncIterable
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from domain.interface.transaction_manager.transaction_manager import TransactionManagerProtocol
from infrastructure.persistence.database import Database
from infrastructure.persistence.transaction_manager import SQLAlchemyTransactionManager
from config import config_manager


class DatabaseProvider(Provider):
    
    @provide(scope=Scope.APP, provides=Database)
    def provide_database(self) -> Database:
        return Database(config_manager.database.URL)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(self, database: Database) -> AsyncIterable[AsyncSession]:
        async with database.get_session() as session:
            yield session

    transaction_manager = provide(SQLAlchemyTransactionManager, provides=TransactionManagerProtocol, scope=Scope.REQUEST)
    
