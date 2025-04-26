class DomainException(Exception):
    """Base class for all domain exceptions."""
    pass

class AlreadyExistException(DomainException):
    """Exception raised when an entity or value-object already exists in the domain."""
    pass

class InvalidValueException(DomainException):
    """Exception raised when an invalid value is encountered."""
    pass

class NotFoundException(DomainException):
    """Exception raised when an entity or value-object is not found in the domain."""
    pass
