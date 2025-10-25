from dishka import Provider, Scope, provide
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


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    register_user_interactor = provide(RegisterUserInteractor)
    login_user_interactor = provide(LoginUserInteractor)
    logout_user_interactor = provide(LogoutUserInteractor)
    delete_user_interactor = provide(DeleteUserInteractor)
    forgot_password_interactor = provide(ForgotPasswordInteractor)
    reset_password_interactor = provide(ResetPasswordInteractor)
    update_email_interactor = provide(UpdateEmailInteractor)
    update_role_interactor = provide(UpdateRoleInteractor)
    get_current_user_info_interactor = provide(GetCurrentUserInfoInteractor)
    generate_access_token_from_refresh_interactor = provide(GenerateAccessTokenFromRefreshInteractor)
