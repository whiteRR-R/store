from fastapi import APIRouter, status, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from domain.interface.usecases.auth_usecase import AuthUseCaseInterface
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO
from application.dtos.user_dto import UserDTO
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.dtos.reset_password_dto import ResetPasswordDTO
from presentation.responses.jwt_token_response import JWTTokenResponse
from presentation.responses.forgot_password_response import ForgotPasswordResponse
from presentation.responses.reset_password_response import ResetPasswordResponse
from presentation.responses.user_data_response import UserDataResponse
from presentation.responses.register_response import RegisterResponse
from presentation.decorators.http_exception import handle_http_exception


class AuthController:
    http_bearer = HTTPBearer(auto_error=False)
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
    
    def __init__(self, auth_usecase: AuthUseCaseInterface):
        self.auth_usecase = auth_usecase
        self.router = APIRouter(dependencies=[Depends(self.http_bearer)])
        
        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
            response_model=RegisterResponse
        )
        
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
            response_model=JWTTokenResponse
        )
        
        self.router.add_api_route(
            "/forgot_password",
            self.forgot_password,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
            response_model=ForgotPasswordResponse
        )
        
        self.router.add_api_route(
            "/reset_password",
            self.reset_password,
            methods=["PUT"],
            status_code=status.HTTP_200_OK,
            response_model=ResetPasswordResponse,
        )
        
        self.router.add_api_route(
            "/refresh",
            self.auth_refresh_token,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
            response_model=JWTTokenResponse,
            response_model_exclude_none=True
        )
        
        self.router.add_api_route(
            "/me",
            self.get_user_data,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
            response_model=UserDataResponse
        )

    @handle_http_exception    
    async def register(self, user_dto: UserDTO) -> RegisterResponse:
        await self.auth_usecase.register(user_dto)
        return RegisterResponse(message="User successfully registered")
    
    @handle_http_exception
    async def login(self, login_dto: UserLoginDTO = Form()) -> JWTTokenResponse:
        user_tokens = await self.auth_usecase.login(login_dto)
        return JWTTokenResponse(
            access_token=user_tokens.access_token,
            refresh_token=user_tokens.refresh_token,
        )
    
    @handle_http_exception
    async def forgot_password(self, forgot_dto: ForgotPasswordDTO = Form()) -> ForgotPasswordResponse:
        reset_token = await self.auth_usecase.forgot_password(forgot_dto)
        return ForgotPasswordResponse(email=forgot_dto.email, reset_token=reset_token)
    
    @handle_http_exception
    async def reset_password(self, reset_dto: ResetPasswordDTO) -> ResetPasswordResponse:
        await self.auth_usecase.reset_password(reset_dto)
        return ResetPasswordResponse(message="Password successfully resetted")
        
    @handle_http_exception
    async def auth_refresh_token(self, jwt_dto: JWTTokenDTO) -> JWTTokenResponse:
       access_token = await self.auth_usecase.generate_access_token_from_refresh(jwt_dto)
       return JWTTokenResponse(access_token=access_token)
    
    @handle_http_exception
    async def get_user_data(self, jwt_token: str=Depends(oauth2_scheme)) -> UserDataResponse:
        user_info = await self.auth_usecase.get_current_user_info(jwt_token)
        return user_info
