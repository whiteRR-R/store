from abc import abstractmethod, ABC


class AuthServiceInterface(ABC):
    @abstractmethod
    async def register_user(self):
        pass

    @abstractmethod
    async def login_user(self):
        pass