from operator import methodcaller
from typing import Literal

from pydantic import UUID4
from sqlalchemy import select, delete, update, and_

from db import Database
from utils import Pagination

__all__ = ("CrudOperations", )


class CrudOperations:
    """ class for generic CRUD operations """

    def __init__(self, *, db: Database):
        self.db = db

    async def create_resource(self, resource):
        session = await self.db.get_session()

        async with session.begin():
            session.add(resource)
            await session.commit()

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

    async def update_resource(self, resource, *, resource_id: UUID4, _filter=None,  **fields_to_update):
        resource_id_filter = resource.id == resource_id

        if _filter is None:
            _filter = resource_id_filter
        else:
            _filter = and_(resource_id_filter, _filter)

        session = await self.db.get_session()

        async with session.begin():
            statement = update(resource). \
                filter(_filter). \
                values(**fields_to_update)

            result = await session.execute(statement)
            await session.commit()
            return result.rowcount

    async def delete_resource(self, resource, *, filter_) -> int:
        session = await self.db.get_session()

        async with session.begin():
            statement = delete(resource).filter(filter_)
            result = await session.execute(statement)
            await session.commit()
            return result.rowcount  # number of rows affected by deletion

    # other operations
    # TODO -> make its own dedicated class for non-crud operations?
    async def get_count(self, resource, *, filter_=None):  # TODO: probably can be optimized
        session = await self.db.get_session()

        async with session.begin():
            statement = select(resource) \
                if filter_ is None \
                else select(resource).filter(filter_)

            resource_count = sum(1 for _ in (await session.execute(statement)))
        return resource_count
