from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


class SQLAlchemyDatabase:
    def __init__(self, URL: str):
        self._URL = URL
        self._engine = create_async_engine(self._URL, echo=True)
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)

    async def get_session(self):
        """Get a new session for database operations."""
        async with self._session_maker() as session:
            yield session

    async def close(self):
        """Close the database connection."""
        await self._engine.dispose()


