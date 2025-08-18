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
        session: AsyncSession
    ):
        self.user_datamapper = UserDataMapper()
        self.session = session
    
    async def add(self, user: User) -> None:
        """Добавляет пользователя в базу данных."""
        model = self.user_datamapper.from_entity(user)
        self.session.add(model)

    async def update(self, user: User) -> None:
        """Обновляет данные пользователя."""
        stmt = (
            update(UserModel)
            .where(UserModel.username == user.username)
            .values(
                email=user.email,
                hashed_password=user.hash_password,
                role=user.role
            )
        )
        await self.session.execute(stmt)

    async def delete(self, username: str) -> None:
        """Удаляет пользователя по username."""
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = stmt.scalar_one_or_none()
        if user:
            await self.session.delete(user)

    async def get_by_username(self, username: str) -> Optional[User]:
        """ Находит пользователя по его имени (username). """
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = stmt.scalar_one_or_none()
        return self.user_datamapper.to_entity(user) if user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """ Находит пользователя по его почте (email). """
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = stmt.scalar_one_or_none()
        return self.user_datamapper.to_entity(user) if user else None
