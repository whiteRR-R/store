from uuid import uuid4
from application.dtos.user_dto import UserDTO, UserGatewayDTO
from domain.entities.user import User
from domain.enums.role import Role
from domain.valueobject.email import Email
from domain.valueobject.username import Username


class UserFactory:
    """ Фабрика для создания пользователей """

    @staticmethod
    def from_params(username: str, role: Role, email: str, hash_password: bytes) -> User:
        """ Создает нового пользователя """
        return User(
            user_id=uuid4(),
            username=Username(username),
            role=role,
            email=Email(email),
            hash_password=hash_password
        )

    @staticmethod
    def from_dto(user_dto: UserDTO, hashed_password: bytes) -> User:
        return User(
            user_id=uuid4(),
            username=Username(user_dto.username),
            role=user_dto.role,
            email=Email(user_dto.email),
            hash_password=hashed_password
        )

    @staticmethod
    def to_dto(user: User) -> UserDTO:
        return UserDTO(
            username=user.username,
            email=user.email,
            password=user.hash_password.decode("utf-8"),
            role=user.role
            )
    
