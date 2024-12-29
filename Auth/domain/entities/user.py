from domain.valueobject.role import Role
from domain.valueobject.email import Email
from domain.valueobject.username import Username
from domain.valueobject.permission import Permission

class User:
    """Доменная модель пользователя"""
    def __init__(self, username: Username, role: Role, email: Email, password_hash: str):
        self.username = username
        self.role = role
        self.email = email
        self.password_hash = password_hash  
