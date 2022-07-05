from operator import methodcaller
from typing import Literal

from sqlalchemy import select

from ..db import Database
from ..utils import Pagination

__all__ = ("CrudOperations", )


class CrudOperations:
    """ class for generic CRUD operations """

    def __init__(self, *, db: Database):
        self.db = db

    async def create_resource(self, resource):
        session = await self.db.get_session()

        async with session.begin():
            session.add(resource)
            session.commit()

    async def read_resource(
            self,
            resource,
            *,
            filter_=None,
            method: Literal["all", "first", "one", "one_or_none"] = "first",
            pagination: Pagination = None  # will be used for pagination if provided
    ):
        session = await self.db.get_session()

        async with session.begin():

            # filter
            statement = select(resource) \
                if filter_ is None \
                else select(resource).filter(filter_)

            # pagination
            if pagination is not None and isinstance(pagination, Pagination):
                statement = statement. \
                    offset(pagination.offset). \
                    limit(pagination.limit)

            call_with_method = methodcaller(method)
            # EXAMPLE:
            #
            # if:
            #   call_with_method == methodcaller("all")
            # then this will be executed:
            #   session.execute(stmt).scalars().all()
            #
            return call_with_method(
                (await session.execute(statement)).scalars()
            )

    async def update_resource(self, resource_id: int, **fields_to_update):
        return NotImplemented

    async def delete_resource(self, resource_id: int):
        return NotImplemented
