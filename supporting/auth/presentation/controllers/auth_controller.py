from typing import Annotated
from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from application.dtos.change_email import ChangeEmailDTO
from domain.interface.usecases.auth_usecase import AuthUseCaseProtocol
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokensDTO
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
from presentation.responses.change_email_response import ChangeEmailResponse
from container import Container


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_dto: UserDTO,
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    await auth_usecase.register(user_dto)
    return RegisterResponse(message="User successfully registered")


@router.post("/login", response_model=JWTTokenResponse, status_code=status.HTTP_201_CREATED)
@inject
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase]),
):
    user_dto = UserLoginDTO(username=form_data.username, password=form_data.password)
    tokens: JWTTokensDTO = await auth_usecase.login(user_dto)
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
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    await auth_usecase.logout(token, refresh_token)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return LogoutUserResponse(message="User successfully logged out")


@router.delete("/delete", response_model=DeleteUserResponse, status_code=status.HTTP_200_OK)
@inject
async def delete_account(
    response: Response,
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    await auth_usecase.delete(token)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return DeleteUserResponse(message="User successfully deleted")


@router.post("/forgot_password", response_model=ForgotPasswordResponse, status_code=status.HTTP_201_CREATED)
@inject
async def forgot_password(
    forgot_dto: ForgotPasswordDTO,
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    reset_token = await auth_usecase.forgot_password(forgot_dto)
    return ForgotPasswordResponse(email=forgot_dto.email, reset_token=reset_token)


@router.put("/reset_password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
@inject
async def reset_password(
    reset_dto: ResetPasswordDTO,
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    await auth_usecase.reset_password(reset_dto)
    return ResetPasswordResponse(message="Password successfully reset")


@router.put("/change_email", response_model=ChangeEmailResponse, status_code=status.HTTP_200_OK)
@inject
async def change_email(
    change_email_dto: ChangeEmailDTO,
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    await auth_usecase.update_email(token, change_email_dto)
    return ChangeEmailResponse(message=f"Email successfully changed to {change_email_dto.new_email}")


@router.post("/refresh", response_model=JWTTokenResponse, status_code=status.HTTP_201_CREATED)
@inject
async def refresh_tokens(
    request: Request,
    response: Response,
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    access_token = await auth_usecase.generate_access_token_from_refresh(refresh_token)
    response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="lax")
    return JWTTokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserDataResponse, status_code=status.HTTP_200_OK)
@inject
async def get_user_data(
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCaseProtocol = Depends(Provide[Container.auth_usecase])
):
    user = await auth_usecase.get_current_user_info(token)
    return UserDataResponse(username=user.username, email=user.email, role=user.role)
