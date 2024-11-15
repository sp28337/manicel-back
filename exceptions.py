class UserNotFoundException(Exception):
    detail = "User not found"


class UserIncorrectPasswordException(Exception):
    detail = "Incorrect password"


class UserAlreadyExistsException(Exception):
    detail = "User with this name already exists"
