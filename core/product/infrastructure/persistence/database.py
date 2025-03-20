from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass


class Database:
    """Класс для управления подключением к базе данных sqlalchemy"""
    def __init__(self, database_url: str):
        self._database_url = database_url
        self._engine = create_async_engine(
            url=self._database_url
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine
        )
    
    async def get_session(self):
        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
            finally:
                await session.close()
        