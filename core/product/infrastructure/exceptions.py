class InfrastructureException(Exception):
    """Base class for all exceptions in the infrastructure module."""
    pass


class DatabaseConnectionError(InfrastructureException):
    """Exception raised when there is a database connection error."""
    pass

class RollbackException(InfrastructureException):
    """Exception raised when a transaction rollback is required."""
    pass

class NotFoundException(InfrastructureException):
    """Exception raised when an entity is not found."""
    pass
