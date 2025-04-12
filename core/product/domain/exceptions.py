class DomainException(Exception):
    pass

class AlreadyExistException(DomainException):
    pass

class InvalidValueException(DomainException):
    pass
