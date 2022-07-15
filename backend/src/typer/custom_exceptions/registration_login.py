from fastapi import HTTPException, status


class UserAlreadyRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user is already registered"
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid credentials"
        )


class ActivationTokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="activation token does not exist"
        )


class AccountAlreadyActivatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="account is already activated"
        )


class AccountNotActivatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="account is not activated"
        )


class ActivationLinkExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="activation link is expired"
        )


class MissingCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="password along with email or name must be provided"
        )


__all__ = [
    item for item in dir()
    if str(item)[0].isupper() and not str(item).startswith("HTTP")
]
