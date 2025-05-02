from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from infrastructure.exceptions import RollbackException


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass


class Database:
    """Class for managing the database connection and session"""
    def __init__(self, database_url: str):
        self._database_url = database_url
        self._engine = create_async_engine(
            url=self._database_url
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine
        )
    
    @asynccontextmanager
    async def get_session(self):
        session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise RollbackException("Transaction rollbacked")
        finally:
            await session.close()
