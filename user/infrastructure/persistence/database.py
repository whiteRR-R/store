from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



class SQLAlchemyDatabase:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.session_factory = async_sessionmaker(bind=self.engine)

    @asynccontextmanager
    async def get_session(self):
        session = self.session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
