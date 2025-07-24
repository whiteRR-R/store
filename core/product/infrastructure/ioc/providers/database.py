from typing import AsyncIterable
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from infrastructure.persistence.database.database import Database
from infrastructure.persistence.database.transaction_manager import SQLAlchemyTransactionManager
from infrastructure.storage.s3_storage import S3ImageStorage

class DatabaseProvider(Provider):
    def __init__(self, database_url: str):
        super().__init__()
        self._database = Database(database_url)
    
    @provide(scope=Scope.APP)
    def provide_database(self) -> Database:
        return self._database
        
    @provide(scope=Scope.REQUEST)
    async def provide_session(self, database: Database) -> AsyncIterable[AsyncSession]:
        async with database.get_session() as session:
            yield session
    
    transaction_manager = provide(
        SQLAlchemyTransactionManager,
        provides=TransactionManagerProcotol,
        scope=Scope.REQUEST
    )
