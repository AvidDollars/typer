from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, status
from fastapi.requests import Request

from ..containers import Container
from ..models.text_rating import TextRatingIn, TextRatingDb
from ..services import TextRatingService
from ..services.auth_service import required_authentication

router = APIRouter(
    prefix="/text-ratings", tags=["Text Ratings"]
)


@router.post(
    "",
    dependencies=[Depends(required_authentication)],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def add_text_rating(
        request: Request,
        text: TextRatingIn,
        text_rating_service: TextRatingService = Depends(Provide[Container.text_rating_service])
):
    text_rating = TextRatingDb(**text.dict(), rated_by=request.user_id)
    await text_rating_service.insert_text_rating(text_rating=text_rating)
