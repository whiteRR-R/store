from fastapi import APIRouter
from domain.interface.usecases.auth_use_case import AuthUseCaseInterface
from application.dtos.register_dto import UserRegisterRequest, UserRegisterResponse
from application.dtos.login_dto import UserLoginRequest, UserLoginResponse


class AuthController:
    def __init__(self, auth_use_case: AuthUseCaseInterface):
        self.auth_use_case = auth_use_case
        self.router = APIRouter()
        
        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            response_model=UserRegisterResponse
        )
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=UserLoginResponse
        )
        
    async def register(self, user: UserRegisterRequest) -> UserRegisterResponse:
        await self.auth_use_case.register(
            username=user.username,
            role=user.role,
            email=user.email,
            password=user.password
        )
        return UserRegisterResponse()
    
    async def login(self, user: UserLoginRequest) -> UserLoginResponse:
        user_data = await self.auth_use_case.login(username=user.username, password=user.password)
        return UserLoginResponse(
            username=user.username,
            access_token=user.access_token,
            refresh_token=user.refresh_token,
            )