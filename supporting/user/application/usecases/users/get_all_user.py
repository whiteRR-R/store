from application.dtos.user import UserDTO
from application.factories.user_factory import UserFactory
from domain.interfaces.repositories.user_repository import UserRepository


class GetAllUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self) -> list[UserDTO]:
        users = await self.user_repository.get_all()
        return [UserFactory.to_dto(user) for user in users]

