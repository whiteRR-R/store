class ApplicationException(Exception):
    pass

class AuthException(ApplicationException):
    """ Исключение для ошибок аутентификации """
    pass

class RegistrationException(ApplicationException):
    """ Исключение для ошибок регистрации """
    pass

class AlreadyExistsException(RegistrationException):
    """ Исключение для случаем если уже существует какая небудь сущность """
    pass

class UserNotFoundException(AuthException):
    """ Исключение если пользователь не найден """
    pass

class TokenProcessingException(ApplicationException):
    pass