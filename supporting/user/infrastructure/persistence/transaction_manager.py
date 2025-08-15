from sqlalchemy.ext.asyncio import AsyncSession
from domain.interfaces.transaction_manager import TransactionManager


class SQLAlchemyTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
