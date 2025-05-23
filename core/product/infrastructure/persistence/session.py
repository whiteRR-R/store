from infrastructure.persistence.database import Database
from sqlalchemy.ext.asyncio import AsyncSession


async def provide_session(db: Database) -> AsyncSession: # type: ignore
    """Provides a session for the database"""
    async with db.get_session() as session:
        yield session
