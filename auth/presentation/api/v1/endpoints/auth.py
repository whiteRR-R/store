from typing import Annotated
from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dishka.integrations.fastapi import FromDishka, inject
from application.usecase.auth.register_user import RegisterUserInteractor
from application.usecase.auth.login_user import LoginUserInteractor
from application.usecase.auth.logout_user import LogoutUserInteractor
from application.usecase.auth.delete_user import DeleteUserInteractor
from application.usecase.auth.forgot_password import ForgotPasswordInteractor
from application.usecase.auth.reset_password import ResetPasswordInteractor
from application.usecase.auth.update_email import UpdateEmailInteractor
from application.usecase.auth.update_role import UpdateRoleInteractor
from application.usecase.auth.get_current_user_info import GetCurrentUserInfoInteractor
from application.usecase.auth.generate_access_token_from_refresh import GenerateAccessTokenFromRefreshInteractor
from application.dtos.change_email import ChangeEmailDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO, JWTTokensDTO
from application.dtos.user_dto import UserDTO
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.dtos.reset_password_dto import ResetPasswordDTO
from presentation.responses.jwt_token_response import JWTTokenResponse
from presentation.responses.forgot_password_response import ForgotPasswordResponse
from presentation.responses.reset_password_response import ResetPasswordResponse
from presentation.responses.user_data_response import UserDataResponse
from presentation.responses.register_response import RegisterResponse
from presentation.responses.delete_user_response import DeleteUserResponse
from presentation.responses.logout_user_response import LogoutUserResponse


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_dto: UserDTO,
    auth_usecase: FromDishka[RegisterUserInteractor],
):
    await auth_usecase(user_dto)
    return RegisterResponse(message="User successfully registered")


@router.post("/login", response_model=JWTTokenResponse, status_code=status.HTTP_201_CREATED)
@inject
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_usecase: FromDishka[LoginUserInteractor],
):
    user_dto = UserLoginDTO(username=form_data.username, password=form_data.password)
    tokens: JWTTokensDTO = await auth_usecase(user_dto)
    response.set_cookie("access_token", tokens.access_token, httponly=True, secure=True, samesite="lax")
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True, secure=True, samesite="lax")
    return JWTTokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type="bearer"
    )


@router.post("/logout", response_model=LogoutUserResponse, status_code=status.HTTP_200_OK)
@inject
async def logout(
    request: Request,
    response: Response,
    auth_usecase: FromDishka[LogoutUserInteractor],
    token: str = Depends(oauth2_scheme),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    await auth_usecase(token, refresh_token)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return LogoutUserResponse(message="User successfully logged out")


@router.delete("/delete", response_model=DeleteUserResponse, status_code=status.HTTP_200_OK)
@inject
async def delete_account(
    response: Response,
    auth_usecase: FromDishka[DeleteUserInteractor],
    token: str = Depends(oauth2_scheme),
):
    await auth_usecase(JWTTokenDTO(token=token))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return DeleteUserResponse(message="User successfully deleted")


@router.post("/forgot_password", response_model=ForgotPasswordResponse, status_code=status.HTTP_201_CREATED)
@inject
async def forgot_password(
    auth_usecase: FromDishka[ForgotPasswordInteractor],
    forgot_dto: ForgotPasswordDTO,
):
    reset_token = await auth_usecase(forgot_dto)
    return ForgotPasswordResponse(email=forgot_dto.email, reset_token=reset_token)


@router.put("/reset_password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
@inject
async def reset_password(
    auth_usecase: FromDishka[ResetPasswordInteractor],
    reset_dto: ResetPasswordDTO,
):
    await auth_usecase(reset_dto)
    return ResetPasswordResponse(message="Password successfully reset")


@router.post("/refresh", response_model=JWTTokenResponse, status_code=status.HTTP_201_CREATED)
@inject
async def refresh_tokens(
    auth_usecase: FromDishka[GenerateAccessTokenFromRefreshInteractor],
    request: Request,
    response: Response,
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    access_token = await auth_usecase(JWTTokenDTO(token=refresh_token))
    response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="lax")
    return JWTTokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/validate", response_model=UserDataResponse, status_code=status.HTTP_200_OK)
@inject
async def get_user_data(
    auth_usecase: FromDishka[GetCurrentUserInfoInteractor],
    token: str = Depends(oauth2_scheme),
):
    user = await auth_usecase(token)
    return UserDataResponse(username=user.username, email=user.email, role=user.role.value)
