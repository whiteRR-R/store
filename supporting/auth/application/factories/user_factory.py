from domain.entities.user import User
from domain.valueobject.role import Role
from domain.valueobject.email import Email
from domain.valueobject.username import Username


class UserFactory:
    """ Фабрика для создания пользователей """

    @staticmethod
    def create(username: str, role: str, email: str, hash_password: bytes) -> User:
        """ Создает нового пользователя """
        return User(
            username=Username(username),
            role=Role(role),
            email=Email(email),
            hash_password=hash_password
        )
