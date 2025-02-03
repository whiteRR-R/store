from fastapi import APIRouter, status, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from domain.interface.usecases.auth_usecase import AuthUseCaseInterface
from application.dtos.register_dto import UserRegisterRequest, UserRegisterResponse
from application.dtos.login_dto import UserLoginRequest
from application.dtos.jwt_token_dto import JWTTokenResponse
from application.dtos.user_dto import UserDataResponse
from application.dtos.forgot_password_dto import ForgotPasswordRequest, ForgotPasswordResponse
from application.dtos.reset_password_dto import ResetPasswordRequest, ResetPasswordResponse
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
            response_model=UserRegisterResponse
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
            methods=["PATCH"],
            status_code=status.HTTP_200_OK,
            response_model=ResetPasswordResponse
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
    async def register(self, user: UserRegisterRequest) -> UserRegisterResponse:
        await self.auth_usecase.register(
            username=user.username,
            role=user.role,
            email=user.email,
            password=user.password
        )
        return UserRegisterResponse()
    
    @handle_http_exception
    async def login(
        self,
        login_scheme: UserLoginRequest = Form()
    ) -> JWTTokenResponse:
        user_tokens = await self.auth_usecase.login(username=login_scheme.username, password=login_scheme.password)
        return JWTTokenResponse(
            access_token=user_tokens.access_token,
            refresh_token=user_tokens.refresh_token,
        )
    
    @handle_http_exception
    async def forgot_password(self, email: ForgotPasswordRequest = Form()) -> ForgotPasswordResponse:
        reset_token = await self.auth_usecase.forgot_password(email)
        return ForgotPasswordResponse(email=email, reset_token=reset_token)
    
    @handle_http_exception
    async def reset_password(self, reset_scheme: ResetPasswordRequest) -> ResetPasswordResponse:
        await self.auth_usecase.reset_password(reset_scheme.reset_token, reset_scheme.new_password)
        return ResetPasswordResponse("Password successfully resetted")
        
    @handle_http_exception
    async def auth_refresh_token(self, jwt_token: str) -> JWTTokenResponse:
       access_token = await self.auth_usecase.generate_access_token_from_refresh(jwt_token)
       return JWTTokenResponse(access_token=access_token)
    
    @handle_http_exception
    async def get_user_data(self, jwt_token: str=Depends(oauth2_scheme)) -> UserDataResponse:
        user_info = await self.auth_usecase.get_current_user_info(jwt_token)
        return user_info