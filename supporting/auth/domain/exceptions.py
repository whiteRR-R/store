class DomainException(Exception):
    pass


class InvalidRoleException(DomainException):
    pass


class InvalidEmailException(DomainException):
    pass


class InvalidUsernameException(DomainException):
    pass


class InvalidPermissionException(DomainException):
    pass
