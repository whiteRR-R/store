from domain.entities.user import User
from domain.abstacts.repository.base_repository import IBaseRepository
from infrastructure.persistence.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class SqlAlchemyAuthRepository(IBaseRepository):
    """Инициализация Sqlalchemy Auth Repository репозитория."""
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> UserModel:
        """Создает нового пользователя в базе данных."""
        new_user = UserModel(
            username=user.username,
            role=user.role,
            email=user.email,
            password_hash=user.password_hash
        )
        self.session.add(new_user)
        
    async def find_by_username(self, username: str) -> Optional[UserModel]:
        """Находит пользователя по его имени (username)."""
        stmt = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = stmt.one_or_none()
        return user
           
        
