from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user import User
from domain.interfaces.repositories.user_repository import UserRepository
from infrastructure.exceptions import UserNotFoundException
from infrastructure.persistence.models.user_model import UserModel
from infrastructure.persistence.datamappers.user_datamapper import UserDataMapper


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_datamapper = UserDataMapper()

    async def add(self, user: User):
        user_model = self.user_datamapper.to_model(user)
        self.session.add(user_model)
        print(user_model)
        print(user_model.id)

    async def update(self, user: User):
        stmt = select(UserModel).where(UserModel.id == user.user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        if not user_model:
            raise UserNotFoundException(f"User with id {user.user_id} not found")
        user_model.username = user.username
        user_model.email = user.email
        user_model.password = user.hashed_password
        user_model.role = user.role
        user_model.status = user.status
    
    async def get_by_id(self, user_id: UUID):
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        return self.user_datamapper.to_entity(user_model) if user_model else None
    
    async def get_all(self):
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        user_models = result.scalars().all()
        return [self.user_datamapper.to_entity(user_model) for user_model in user_models]
