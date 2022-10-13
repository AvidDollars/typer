from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import Response

from ..containers import Container
from ..models import TextRatingIn, TextRatingDb, TextRatingUpdate
from ..services import TextRatingService
from ..services.auth_service import required_authentication

router = APIRouter(
    prefix="/text-ratings", tags=["Text Ratings"], dependencies=[Depends(required_authentication)]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def add_text_rating(
        request: Request,
        text_rating: TextRatingIn,
        text_rating_service: TextRatingService = Depends(Provide[Container.text_rating_service])
):
    text_rating = TextRatingDb(**text_rating.dict(), rated_by=request.user_id)
    await text_rating_service.insert_text_rating(text_rating=text_rating)


@router.patch("/")
@inject
async def update_text_rating(
    request: Request,
    text_rating: TextRatingUpdate,
    text_rating_service: TextRatingService = Depends(Provide[Container.text_rating_service])
):
    text_rating = TextRatingDb(**text_rating.dict(), rated_by=request.user_id)
    await text_rating_service.update_text_rating(text_rating=text_rating)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
