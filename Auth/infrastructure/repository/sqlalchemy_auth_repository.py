from domain.entities.user import User
from domain.interface.repository.sqlalchemy_auth_repository import SqlAlchemyAuthRepositoryInterface
from infrastructure.persistence.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, update
from typing import Optional


class SqlAlchemyAuthRepository(SqlAlchemyAuthRepositoryInterface):
    """ Инициализация Sqlalchemy Auth Repository репозитория. """
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> UserModel:
        """ Создает нового пользователя в базе данных. """
        new_user = UserModel(user)
        self.session.add(new_user)
        
    async def find_by_username(self, username: str) -> Optional[UserModel]:
        """ Находит пользователя по его имени (username). """
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = stmt.scalar_one_or_none()
        return user
    
    async def find_by_email(self, email: str) -> Optional[UserModel]:
        """ Находит пользователя по его почте (email). """
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = stmt.scalar_one_or_none()
        return user

    async def update(self, user: User):
        """ Обновляет данные пользователя """
        update_data = {
            "username": user.username.value,
            "email": user.email.value,
            "role": user.role.value,
            "hashed_password": user.hash_password
        }
        
        result = await self.session.execute(
            update(UserModel)
            .where(UserModel.username == user.username)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        
        if result.rowcount == 0:
            raise NoResultFound(f"User with id {user.username} not found.")

