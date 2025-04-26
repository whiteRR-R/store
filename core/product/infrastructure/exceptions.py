class InfrastructureException(Exception):
    """Base class for all exceptions in the infrastructure module."""
    pass

class DataNotFoundError(InfrastructureException):
    """Exception raised when data is not found in the database."""
    pass

class DatabaseConnectionError(InfrastructureException):
    """Exception raised when there is a database connection error."""
    pass
