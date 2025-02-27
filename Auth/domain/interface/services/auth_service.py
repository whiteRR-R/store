from abc import abstractmethod, ABC
from application.dtos.login_dto import UserLoginDTO
from application.dtos.user_dto import UserDTO


class AuthServiceInterface(ABC):
    @abstractmethod
    async def create_user(self, user_dto: UserDTO):
        raise NotImplementedError
    
    @abstractmethod
    async def _existing_username_or_email(self, username: str, email: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_user_credentials(self, user_credentials: UserLoginDTO):
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_by_username(self, username: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_by_email(self, email: str):
        raise NotImplementedError
    
