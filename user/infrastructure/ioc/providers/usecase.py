from dishka import Provider, Scope, provide

from application.usecases.address.add_address import AddUserAddressUseCase
from application.usecases.address.delete_address import DeleteUserAddressUseCase
from application.usecases.users.create_user import UserCreateUseCase
from application.usecases.address.get_user_address import GetUserAddressUseCase
from application.usecases.users.get_user_by_id import GetUserByIDUseCase
from application.usecases.users.get_all_user import GetAllUsersUseCase
from application.usecases.address.update_address import UpdateUserAddressUseCase
from application.usecases.users.update_user_email import UpdateUserEmailUseCase


class UseCaseProvider(Provider):
    scope = Scope.REQUEST
    
    # user
    create_user_usecase = provide(UserCreateUseCase)
    get_user_by_id_usecase = provide(GetUserByIDUseCase)
    user_get_all_usecase = provide(GetAllUsersUseCase)
    update_user_email_usecase = provide(UpdateUserEmailUseCase)
    get_user_address_usecase = provide(GetUserAddressUseCase)
    # address
    add_user_address_usecase = provide(AddUserAddressUseCase)
    update_user_address_usecase = provide(UpdateUserAddressUseCase)
    delete_user_address_usecase = provide(DeleteUserAddressUseCase)
