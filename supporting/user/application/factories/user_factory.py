from application.dtos.user import UserCreateDTO, UserDTO
from domain.entities.user import User, UserRole, UserStatus


class UserFactory:
    @staticmethod
    def from_dto(user_dto: UserCreateDTO) -> User:
        return User(
            user_id=user_dto.user_id,
            username=user_dto.username,
            email=user_dto.email,
            hashed_password=user_dto.hashed_password,
            role=UserRole(user_dto.role),
            status=UserStatus(user_dto.status)
        )

    @staticmethod
    def to_dto(user: User) -> UserDTO:
        return UserDTO(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role.value,
            status=user.status.value
        )
