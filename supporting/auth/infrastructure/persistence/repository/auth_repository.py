from typing import Optional, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from domain.entities.user import User
from infrastructure.persistence.data_mapper.user_datamapper import UserDataMapper
from infrastructure.persistence.models.user_model import UserModel


class SQLAlchemyAuthRepository:
    """ Инициализация Sqlalchemy Auth Repository репозитория. """
    def __init__(
        self,
        user_data_mapper: UserDataMapper,
        session_context_manager: AsyncContextManager[AsyncSession]
    ):
        self.user_data_mapper = user_data_mapper
        self.session = session_context_manager
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """ Находит пользователя по его имени (username). """
        async with self.session as session:
            stmt = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user = stmt.scalar_one_or_none()
            return self.user_data_mapper.to_entity(user) if user else None

    async def find_by_email(self, email: str) -> Optional[User]:
        """ Находит пользователя по его почте (email). """
        async with self.session as session:
            stmt = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = stmt.scalar_one_or_none()
        return self.user_data_mapper.to_entity(user) if user else None
