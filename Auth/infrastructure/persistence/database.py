from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass

class Database:
    """Класс для управления подключением к базе данных sqlalchemy"""
    def __init__(self, database_url: str):
        self._database_url = database_url
        self._engine = create_async_engine(
            url=self._database_url,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
        )
    
    @property
    def session_factory(self):
        return self._session_factory
    
    @asynccontextmanager
    async def get_session(self):
        async with self._session_factory() as session:    
            try:
                yield session
            except Exception:
                await session.rollback()
            finally:
                await session.close()