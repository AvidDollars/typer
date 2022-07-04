from operator import methodcaller
from typing import Literal

from sqlalchemy import select

from ..db import Database

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
            method: Literal["all", "first", "one", "one_or_none"] = "first"
    ):
        session = await self.db.get_session()

        async with session.begin():
            if filter_ is None:
                statement = select(resource)
            else:
                statement = select(resource).filter(filter_)

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