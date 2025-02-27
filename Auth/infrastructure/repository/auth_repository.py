from domain.entities.user import User
from domain.interface.repository.auth_repository import AuthRepositoryInterface
from infrastructure.persistence.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, update
from typing import Optional


class AuthRepository(AuthRepositoryInterface):
    """ Инициализация Sqlalchemy Auth Repository репозитория. """
    def __init__(self, session: AsyncSession):
        self.session = session
        
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
