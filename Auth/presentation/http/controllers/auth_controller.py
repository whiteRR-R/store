from fastapi import APIRouter
from domain.interface.usecases.auth_use_case import AuthUseCaseInterface
from Auth.application.dtos.register_dto import UserRegisterRequest


class AuthController:
    def __init__(self, auth_use_case: AuthUseCaseInterface):
        self.auth_use_case = auth_use_case
        self.router = APIRouter()
        
    async def register(self, user: UserRegisterRequest):
        await self.auth_use_case.register(
            username=user.username,
            role=user.role,
            email=user.email,
            password=user.password
        )

        return "User successfully created"