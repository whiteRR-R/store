from fastapi import APIRouter, status, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from domain.interface.usecases.auth_use_case import AuthUseCaseInterface
from application.dtos.register_dto import UserRegisterRequest, UserRegisterResponse
from application.dtos.login_dto import UserLoginRequest
from application.dtos.jwt_token_dto import JWTTokenResponse
from application.dtos.user_dto import UserDataResponse




class AuthController:
    http_bearer = HTTPBearer(auto_error=False)
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
    
    def __init__(self, auth_use_case: AuthUseCaseInterface):
        self.auth_use_case = auth_use_case
        self.router = APIRouter(dependencies=[Depends(self.http_bearer)])
        
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
            response_model=JWTTokenResponse
        )
        
        self.router.add_api_route(
            "/refresh",
            self.auth_refresh_token,
            methods=["POST"],
            response_model=JWTTokenResponse,
            response_model_exclude_none=True
        )
        
        self.router.add_api_route(
            "/me",
            self.get_user_data,
            methods=["GET"],
            response_model=UserDataResponse
        )
        
    async def register(self, user: UserRegisterRequest) -> UserRegisterResponse:
        try:
            await self.auth_use_case.register(
                username=user.username,
                role=user.role,
                email=user.email,
                password=user.password
            )
            return UserRegisterResponse()
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    async def login(
        self,
        login_scheme: UserLoginRequest = Form()
    ) -> JWTTokenResponse:
        user_tokens = await self.auth_use_case.login(username=login_scheme.username, password=login_scheme.password)
        return JWTTokenResponse(
            access_token=user_tokens.access_token,
            refresh_token=user_tokens.refresh_token,
        )
    
    async def auth_refresh_token(self, jwt_token: str) -> JWTTokenResponse:
       access_token = await self.auth_use_case.generate_access_token_from_refresh(jwt_token)
       return JWTTokenResponse(access_token=access_token)
       
    async def get_user_data(self, jwt_token: str=Depends(oauth2_scheme)) -> UserDataResponse:
        user_info = await self.auth_use_case.get_current_user_info(jwt_token)
        return user_info