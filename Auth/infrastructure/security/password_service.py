import bcrypt
from application.interface.password_security import PasswordSecurityInterface


class PasswordSecurityService(PasswordSecurityInterface):
    """Сервис для хэширования паролей и проверки пароля."""
    
    def get_hash_password(self, password: str):
        """Хэширование пароля с использованием bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=password.encode("utf-8"), salt=salt)
        return hashed_password.decode("utf-8")
    
    def verify_password(stored_hash: str, password: str) -> bool:
        """Проверка пароля."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    

