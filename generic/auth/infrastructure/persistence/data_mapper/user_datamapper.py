from domain.entities.user import User
from domain.enums.role import Role
from application.factories.user_factory import UserFactory
from infrastructure.persistence.models.user_model import UserModel
from infrastructure.persistence.models.user_model import UserModel


class UserDataMapper:
    """Класс для преобразования между доменной сущностью User и ORM-моделью UserModel."""
    
    def from_entity(self, user: User) -> UserModel:
        """Преобразует доменную сущность в ORM-модель."""
        return UserModel(
            username=user.username,
            role=user.role,
            email=user.email,
            hashed_password=user.hash_password
        )

    def to_entity(self, model: UserModel) -> User:
        """Преобразует ORM-модель в доменную сущность."""
        return UserFactory.from_params(
            username=model.username,
            email=model.email,
            role=Role(model.role),
            hash_password=model.hashed_password
        )
