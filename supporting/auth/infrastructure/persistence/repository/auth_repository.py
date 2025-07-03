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
        user_datamapper: UserDataMapper,
        session_context_manager: AsyncContextManager[AsyncSession]
    ):
        self.user_datamapper = user_datamapper
        self.session = session_context_manager
    
    async def add(self, user: User) -> None:
        """Добавляет пользователя в базу данных."""
        async with self.session as session:
            model = self.user_datamapper.from_entity(user)
            session.add(model)
            await session.commit()

    async def update(self, user: User) -> None:
        """Обновляет данные пользователя."""
        async with self.session as session:
            stmt = (
                update(UserModel)
                .where(UserModel.username == user.username)
                .values(
                    email=user.email,
                    hashed_password=user.hash_password,
                    role=user.role
                )
            )
            await session.execute(stmt)

    async def delete(self, username: str) -> None:
        """Удаляет пользователя по username."""
        async with self.session as session:
            stmt = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user = stmt.scalar_one_or_none()
            if user:
                await session.delete(user)

    async def find_by_username(self, username: str) -> Optional[User]:
        """ Находит пользователя по его имени (username). """
        async with self.session as session:
            stmt = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user = stmt.scalar_one_or_none()
            return self.user_datamapper.to_entity(user) if user else None

    async def find_by_email(self, email: str) -> Optional[User]:
        """ Находит пользователя по его почте (email). """
        async with self.session as session:
            stmt = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = stmt.scalar_one_or_none()
        return self.user_datamapper.to_entity(user) if user else None
