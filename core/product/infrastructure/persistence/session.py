from database import Database

async def provide_session(db: Database) -> AsyncSession: # type: ignore
    """Provides a session for the database"""
    async with db.get_session() as session:
        yield session
