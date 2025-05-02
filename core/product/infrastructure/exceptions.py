class InfrastructureException(Exception):
    """Base class for all exceptions in the infrastructure module."""
    pass


class DatabaseConnectionError(InfrastructureException):
    """Exception raised when there is a database connection error."""
    pass

class DataNotFoundException(InfrastructureException):
    """Exception raised when data is not found in the database."""
    pass

class RollbackException(InfrastructureException):
    """Exception raised when a transaction rollback is required."""
    pass

