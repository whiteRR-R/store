from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession



class SqlAlchemyOrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(self):
        self.session.add()
        
