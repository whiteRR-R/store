class InfrastructureException(Exception):
    """ Исключение для ошибок инфраструктуры """
    pass

class DatabaseException(InfrastructureException):
    """ Исключение для ошибок базы данных """
    pass

class UnitOfWorkException(InfrastructureException):
    """ Исключение для ошибок Unit of Work """
    pass

class InvalidTokenException(InfrastructureException):
    """ Исключение для ошибок токена """
    pass

class InvalidTokenTypeException(InfrastructureException):
    """ Исключение для ошибок типа токена """
    pass

class RollbackException(InfrastructureException):
    """ Исключение для отката транзакции """
    pass
