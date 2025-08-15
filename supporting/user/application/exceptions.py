class ApplicationDomainException(Exception):
    pass


class UserNotFoundException(ApplicationDomainException):
    pass

class AddressNotFoundException(ApplicationDomainException):
    pass
