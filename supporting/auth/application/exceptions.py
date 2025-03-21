class ApplicationException(Exception):
    """Базовое исключение для всех ошибок приложения."""
    pass


class AuthException(ApplicationException):
    """Базовое исключение для ошибок аутентификации."""
    pass

class InvalidCredentialsException(AuthException):
    """Исключение при неверных учетных данных."""
    def __init__(self):
        super().__init__("Invalid username or password.")


class UserNotFoundException(AuthException):
    """Исключение, если пользователь не найден."""
    def __init__(self, identifier: str):
        super().__init__(f"User with identifier '{identifier}' not found.")


class RegistrationException(ApplicationException):
    """Базовое исключение для ошибок регистрации."""
    pass

class UsernameAlreadyExistsException(RegistrationException):
    """Исключение, если имя пользователя уже занято."""
    def __init__(self, username: str):
        super().__init__(f"Username '{username}' is already taken.")

class EmailAlreadyExistsException(RegistrationException):
    """Исключение, если email уже зарегистрирован."""
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' is already registered.")


class TokenProcessingException(ApplicationException):
    """Ошибка обработки токенов (JWT и др.)."""
    def __init__(self, message: str = "Error processing token."):
        super().__init__(message)
