from infrastructure.persistence.models.user_model import UserModel
from domain.entities.user import User


class UserDataMapper:
    @staticmethod
    def to_entity(model: UserModel) -> User:
        return User(
            username=model.username,
            email=model.email,
            hashed_password=model.password,
            role=model.role,
            status=model.status
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.user_id,
            username=entity.username,
            email=entity.email,
            password=entity.hashed_password,
            role=entity.role.value,
            status=entity.status.value
        )
