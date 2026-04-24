class UserNotFoundException(Exception):
    detail = "User not found"


class UserIncorrectPasswordException(Exception):
    detail = "Incorrect password"


class UserNameAlreadyExistsException(Exception):
    detail = "User with this name already exists"


class UserEmailAlreadyExistsException(Exception):
    detail = "User with this email already exists"


class TokenExpiredException(Exception):
    detail = "Token expired"


class IncorrectTokenException(Exception):
    detail = "Incorrect Token"


class ProductNotFoundException(Exception):
    detail = "Product not found"


class ProductAlreadyExistsException(Exception):
    detail = "Product already exists"


class PermissionDeniedException(Exception):
    detail = "Permission denied"


class LeadNotFoundException(Exception):
    detail = "Lead not found"
