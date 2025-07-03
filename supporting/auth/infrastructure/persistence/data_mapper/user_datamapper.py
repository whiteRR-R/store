from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from domain.entities.user import User
from domain.factories.user_factory import UserFactory
from domain.entities.user import User
from domain.factories.user_factory import UserFactory
from infrastructure.persistence.models.user_model import UserModel
from infrastructure.persistence.models.user_model import UserModel


class UserDataMapper:
    def __init__(self, session: AsyncSession):
        self.session = session

    def from_entity(self, user: User) -> UserModel:
        """Преобразует доменную сущность в ORM-модель."""
        return UserModel(
            username=user.username,
            role=user.role,
            email=user.email,
            hashed_password=user.hash_password
        )

    def to_entity(self, model: UserModel) -> User:
        """Преобразует ORM-модель в доменную сущность."""
        return UserFactory.create(
            username=model.username,
            email=model.email,
            role=model.role,
            hash_password=model.hashed_password
        )

    async def add(self, user: User) -> None:
        """Добавляет пользователя в базу данных."""
        model = self.from_entity(user)
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
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
