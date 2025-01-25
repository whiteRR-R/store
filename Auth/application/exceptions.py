class AlreadyExistsException(Exception):
    """ Исключение для случаем если уже существует какая небудь сущность """
    pass

class AuthenticationException(Exception):
    """ Исключение для ошибок аутентификации """
    pass

class InvalidTokenException(Exception):
    """ Исключение для ошибок токена """
    pass

class UserNotFoundException(Exception):
    """ Исключение если пользователь не найден """
    pass

