import bcrypt
from application.interface.security.password_security import PasswordSecurityInterface


class PasswordSecurity(PasswordSecurityInterface):
    """Сервис для хэширования паролей и проверки пароля."""
    
    def get_hash_password(self, password: bytes) -> bytes:
        """Хэширование пароля с использованием bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password
    
    def verify_password(self, password: bytes, stored_hash: bytes) -> bool:
        """Проверка пароля."""
        return bcrypt.checkpw(password, stored_hash)