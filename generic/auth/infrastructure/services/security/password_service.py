import bcrypt


class BcryptPasswordHasher:
    """Сервис для хэширования паролей и проверки пароля."""
    
    def hash(self, password: str) -> bytes:
        """Хэширование пароля с использованием bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password
    
    def verify(self, password: str, stored_hash: bytes) -> bool:
        """Проверка пароля."""
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
