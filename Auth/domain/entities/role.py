from typing import List
from domain.valueobject.role import Role
from domain.valueobject.permission import Permission


class Role:
    """Роль пользователя, которая определяет набор разрешений."""
    def __init__(self, role: Role, permission: List[Permission]):
        self.role = role
        self.permission = permission
    
    def has_permission(self, permisson_name: Permission):
        """Проверка наличия разрешения у роли."""
        return any(permission == permisson_name for permission in self.permission)
    
