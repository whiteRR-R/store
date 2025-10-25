from uuid import UUID
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import inject, FromDishka
from application.dtos.user import UserCreateDTO, UserDTO, UserEmailUpdateDTO
from application.dtos.address import AddressDTO, UpdateAddressDTO
from application.usecases.address.add_address import AddUserAddressUseCase
from application.usecases.address.get_user_address import GetUserAddressUseCase
from application.usecases.address.update_address import UpdateUserAddressUseCase
from application.usecases.users.create_user import UserCreateUseCase
from application.usecases.address.delete_address import DeleteUserAddressUseCase
from application.usecases.users.get_user_by_id import GetUserByIDUseCase
from application.usecases.users.get_all_user import GetAllUsersUseCase
from application.usecases.users.update_user_email import UpdateUserEmailUseCase

router = APIRouter()


@router.post("/users", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user: UserCreateDTO,
    user_create_use_case: FromDishka[UserCreateUseCase]
) -> UserDTO:
    return await user_create_use_case(user)


@router.get("/users", response_model=list[UserDTO], status_code=status.HTTP_200_OK)
@inject
async def get_users(
    get_all_users_usecase: FromDishka[GetAllUsersUseCase]
) -> list[UserDTO]:
    return await get_all_users_usecase()


@router.get("/users/{user_id}", response_model=UserDTO, status_code=status.HTTP_200_OK)
@inject
async def get_user_by_id(
    user_id: UUID,
    get_user_by_id_usecase: FromDishka[GetUserByIDUseCase]
) -> UserDTO:
    return await get_user_by_id_usecase(user_id)


@router.get("/users/{user_id}/address", response_model=AddressDTO, status_code=status.HTTP_200_OK)
@inject
async def get_user_address(user_id: UUID, get_user_address_usecase: FromDishka[GetUserAddressUseCase]) -> AddressDTO:
    return await get_user_address_usecase(user_id)


@router.patch("/users/{user_id}", response_model=UserDTO, status_code=status.HTTP_200_OK)
@inject
async def update_user(
    user_id: UUID,
    user: UserEmailUpdateDTO,
    update_user_email_usecase: FromDishka[UpdateUserEmailUseCase]
) -> UserDTO:
    return await update_user_email_usecase(user_id, user)

@router.post("/users/{user_id}/address", response_model=AddressDTO, status_code=status.HTTP_201_CREATED)
@inject
async def add_user_address(
    user_id: UUID,
    address: AddressDTO,
    add_user_address_usecase: FromDishka[AddUserAddressUseCase]
) -> AddressDTO:
    return await add_user_address_usecase(user_id, address)

@router.put("/users/{user_id}/address/{address_id}", response_model=UserDTO, status_code=status.HTTP_200_OK)
@inject
async def update_user_address(
    user_id: UUID,
    address_id: UUID,
    address: UpdateAddressDTO,
    update_user_address_usecase: FromDishka[UpdateUserAddressUseCase]
) -> AddressDTO:
    return await update_user_address_usecase(user_id, address_id, address)

@router.delete("/users/{user_id}/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user_address(
    user_id: UUID,
    address_id: UUID,
    delete_user_address_usecase: FromDishka[DeleteUserAddressUseCase]
):
    return await delete_user_address_usecase(user_id, address_id)

