from fastapi import Query

from . import auto_repr

__all__ = ("Pagination", )


@auto_repr
class Pagination:
    """
    example of usage:

        def get_texts(pagination: Pagination = Depends(), ...):
            ...
    """
    def __init__(
            self,
            page: int | None = Query(default=1, ge=1),
            limit: int | None = Query(default=5, ge=1, le=20)
    ):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit
