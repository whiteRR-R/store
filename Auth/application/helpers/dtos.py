from application.dtos.user_dto import UserDTO
from domain.entities.user import User


def user_dtos_to_user_entitiy(user_dto: UserDTO) -> User:
    username = user_dto.username
    email = user_dto.email
    role = user_dto.role
    hashed_password=  user_dto.password
    user_enitiy = User.create(username=username, email=email, role=role,hash_password=hashed_password)
    return user_enitiy
