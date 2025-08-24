from uuid import uuid4, UUID
from domain.enums.user_status import UserStatus
from domain.enums.role import Role
from domain.valueobject.email import Email
from domain.valueobject.username import Username
from domain.interface.services.hash_service import PasswordHasherProtocol


class User:
    def __init__(
        self, 
        user_id: UUID, 
        username: Username, 
        role: Role, 
        email: Email, 
        hash_password: bytes,
    ):
        self._user_id = user_id
        self._username = username
        self._role = role
        self._email = email
        self._hash_password = hash_password 
    
    def change_email(self, new_email: Email):
        """Обновляет email пользователя"""
        self._email = new_email
    
    def change_role(self, new_role: Role):
        """Обновляет роль пользователя"""
        self._role = new_role

    def verify_password(self, raw_password: str, password_security: PasswordHasherProtocol) -> bool:
        """Проверка пароля"""
        return password_security.verify(raw_password, self._hash_password)

    def set_password(self, raw_password: str, password_security: PasswordHasherProtocol):
        """Хэширует и обновляет пароль"""
        self._hash_password = password_security.hash(raw_password)
        
    @property
    def id(self) -> UUID:
        return self._user_id
    
    @property
    def username(self) -> str:
        return self._username.value
    
    @property
    def role(self) -> Role:
        return self._role
    
    @property
    def email(self) -> str:
        return self._email.value

    @property
    def hash_password(self) -> bytes:
        return self._hash_password

    def __repr__(self):
        return f"User(username={self.username}, role={self.role}, email={self.email})"
