class ApplicationException(Exception):
    """Base class for all application exceptions."""
    pass

class DataNotFoundException(ApplicationException):
    """Exception raised when data is not found."""
    pass
