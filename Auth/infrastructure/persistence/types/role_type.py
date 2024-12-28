from sqlalchemy.types import TypeDecorator, String
from domain.valueobject.role import Role


class RoleType(TypeDecorator):
    """Тип для сериализации и десериализации Role"""
    impl = String

    def process_bind_param(self, value, dialect):
        """Сериализация: преобразуем Role в строку"""
        if isinstance(value, Role):
            return value.role
        return value
    
    def process_result_value(self, value, dialect):
        """Десериализация: преобразуем строку обратно в Role"""
        if value:
            return Role(value)
        return value