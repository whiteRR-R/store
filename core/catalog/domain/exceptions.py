class DomainException(Exception):
    """Base class for exceptions in this module."""
    pass


class EmptyException(DomainException):
    """Raised when the catalog name is empty or contains only whitespace."""
    pass


class TooLongException(DomainException):
    """Raised when the catalog name exceeds the maximum allowed length."""
    pass


class InvalidTypeException(DomainException):
    """Raised when the catalog name is not a string."""
    pass
