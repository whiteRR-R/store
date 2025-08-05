from domain.valueobject.role import Role
from domain.valueobject.email import Email
from domain.valueobject.username import Username
from domain.valueobject.permission import Permission


class User:
    """Доменная модель пользователя"""
    def __init__(self, username: Username, role: Role, email: Email, hash_password: bytes):
        self._username = username
        self._role = role
        self._email = email
        self._hash_password = hash_password  

    def change_password(self, new_hash_password: bytes):
        """ Обновляет пароль пользователя """
        self._hash_password = new_hash_password
    
    def change_email(self, new_email: Email):
        """ Обновляет email пользователя """
        self._email = new_email
    
    def change_role(self, new_role: Role):
        """ Обновляет роль пользователя """
        self._role = new_role
        
    @property
    def username(self):
        return str(self._username)
    
    @property
    def role(self):
        return str(self._role)
    
    @property
    def email(self):
        return str(self._email)
    
    @property
    def hash_password(self):
        return self._hash_password
    
    def __repr__(self):
        return (
            f"User(username={self.username}, role={self.role}, email={self.email})"
        )
