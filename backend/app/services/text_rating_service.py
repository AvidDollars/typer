from ..repositories import CrudOperations
from ..models.text_rating import TextRatingDb, TextRatingUpdate
from sqlalchemy.exc import IntegrityError
from ..constants import UNIQUE_CONSTRAINT_VIOLATED
from fastapi import HTTPException, status


__all__ = ("TextRatingService", )


class TextRatingService:
    def __init__(self, repository: CrudOperations):
        self.repository = repository

    async def insert_text_rating(self, *, text_rating: TextRatingDb):
        try:
            await self.repository.create_resource(text_rating)

        except IntegrityError as error:
            if error.orig.sqlstate == UNIQUE_CONSTRAINT_VIOLATED:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="already rated by the user"
                )

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="text rating not found")
