from domain.entities.role import Role
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
    
    def has_permission(self, permission_name: Permission) -> bool:
        if self.role.has_permission(permission_name):
            return True
        return False
    
    def is_active(self):
        return self.is_active
