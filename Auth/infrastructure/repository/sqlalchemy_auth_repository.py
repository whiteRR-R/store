from domain.entities.user import User
from domain.interface.repository.sqlalchemy_auth_repository import SqlAlchemyAuthRepositoryInterface
from infrastructure.persistence.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class SqlAlchemyAuthRepository(SqlAlchemyAuthRepositoryInterface):
    """ Инициализация Sqlalchemy Auth Repository репозитория. """
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """ Создает нового пользователя в базе данных. """
        new_user = UserModel(user)
        self.session.add(new_user)
        
    async def find_by_username(self, username: str) -> Optional[User]:
        """ Находит пользователя по его имени (username). """
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = stmt.scalar_one_or_none()
        return user.to_domain() if user else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """ Находит пользователя по его почте (email). """
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = stmt.scalar_one_or_none()
        return user.to_domain() if user else None

        
