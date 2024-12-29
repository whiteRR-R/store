from abc import abstractmethod, ABC


class AuthServiceInterface(ABC):
    @abstractmethod
    async def register_user(self, username: str, role: str, email: str, password: str):
        raise NotImplementedError

    @abstractmethod
    async def login_user(self, username: str, password: str):
        raise NotImplementedError
