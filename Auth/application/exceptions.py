class AlreadyExistsException(Exception):
    """ Исключение для случаем если уже существует какая небудь сущность """
    pass

class AuthenticationException(Exception):
    """ Исключение для ошибок аутентификации """
    pass

class UserNotFoundException(Exception):
    """ Исключение если пользователь не найден """
    pass

class RegistrationException(Exception):
    """ Исключение для ошибок регистрации """
    pass