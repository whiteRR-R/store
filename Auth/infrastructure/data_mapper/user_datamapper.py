from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from domain.entities.user import User
from infrastructure.persistence.models.user_model import UserModel



class UserDataMapper:
    def __init__(self, session: AsyncSession):
      self.session = session
      
    async def to_model(self, user: User):
        return UserModel(user)
    
    async def to_entity(self, user_model: UserModel):
        return User.create(
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            role=user_model.role,
        )
    
    async def add(self, user: User):
        user_model = await self.to_model(user)
        self.session.add(user_model)
    
    async def update(self, user: User):
        user_model = await self.to_model(user)
        stmt = (
            update(UserModel)
            .where(UserModel.username == user_model.username)
            .values(
                username=user_model.username,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                role=user_model.role
            )
        )
        await self.session.execute(stmt)
        
    async def delete(self, user: User):
        user_model = await self.to_model(user)
        await self.session.delete(user_model)
