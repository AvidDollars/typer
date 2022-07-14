from fastapi import HTTPException, status


class AlreadyRatedTextException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="already rated by the user"
        )


class TextRatingNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="text rating not found"
        )


class UserTextCountLimitException(HTTPException):
    def __init__(self, max_count):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"user can store {max_count} texts at most"
        )


class TextNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="text not found"
        )


class CantSaveTypingSessionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="unable to save - text or user does not exist"
        )


__all__ = [
    item for item in dir()
    if str(item)[0].isupper() and not str(item).startswith("HTTP")
]