from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class SQLAlchemyDatabase:
    def __init__(self, url: str):
        self._url = url
        self._engine = create_async_engine(self._url)
        self._session_factory = async_sessionmaker(self._engine)

    @asynccontextmanager
    async def get_session(self):
        session = self._session_factory()
        try:
            yield session
        except:
            session.rollback()
