class AuthException(Exception):
    """ Исключение для ошибок аутентификации """
    pass

class RegistrationException(Exception):
    """ Исключение для ошибок регистрации """
    pass

class AlreadyExistsException(RegistrationException):
    """ Исключение для случаем если уже существует какая небудь сущность """
    pass

class UserNotFoundException(AuthException):
    """ Исключение если пользователь не найден """
    pass

class TokenProcessingException(AuthException):
    pass