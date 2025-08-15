from typing import AsyncIterable
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from domain.interfaces.transaction_manager import TransactionManager
from infrastructure.persistence.database import SQLAlchemyDatabase
from infrastructure.persistence.transaction_manager import SQLAlchemyTransactionManager


class DatabaseProvider(Provider):
    def __init__(self, database_url: str):
        super().__init__()
        self._database = SQLAlchemyDatabase(database_url)
    
    @provide(scope=Scope.APP)
    def provide_database(self) -> SQLAlchemyDatabase:
        return self._database
        
    @provide(scope=Scope.REQUEST)
    async def provide_session(self, database: SQLAlchemyDatabase) -> AsyncIterable[AsyncSession]:
        async with database.get_session() as session:
            yield session
    
    transaction_manager = provide(SQLAlchemyTransactionManager, provides=TransactionManager, scope=Scope.REQUEST)
