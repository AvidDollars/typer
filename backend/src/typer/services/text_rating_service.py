from sqlalchemy.exc import IntegrityError

from ..constants import UNIQUE_CONSTRAINT_VIOLATED
from ..custom_exceptions import AlreadyRatedTextException, TextRatingNotFoundException
from ..models.text_rating import TextRatingDb
from ..repositories import CrudOperations

__all__ = ("TextRatingService", )


class TextRatingService:
    def __init__(self, repository: CrudOperations):
        self.repository = repository

    async def insert_text_rating(self, *, text_rating: TextRatingDb):
        try:
            await self.repository.create_resource(text_rating)

        except IntegrityError as error:
            if error.orig.sqlstate == UNIQUE_CONSTRAINT_VIOLATED:
                raise AlreadyRatedTextException

            else:
                raise  # unexpected error... will be logged

    async def update_text_rating(self, *, text_rating: TextRatingDb):
        rows_affected = await self.repository.update_resource(
            TextRatingDb,
            resource_id=text_rating.id,
            _filter=TextRatingDb.rated_by == text_rating.rated_by,
            rating=text_rating.rating
        )

        if not rows_affected:
            raise TextRatingNotFoundException
