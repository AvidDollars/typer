from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import Response
from pydantic import UUID4

from ..containers import Container
from ..models import TextIn, TextDb, TextDetail, TextOut, UserRole
from ..services import TextService
from ..services.auth_service import required_authentication, optional_authentication
from ..utils import Pagination

router = APIRouter(
    prefix="/texts", tags=["Text"]
)


@router.post(
    "/",
    dependencies=[Depends(required_authentication)],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def add_text(
        request: Request,
        text: TextIn,
        text_service: TextService = Depends(Provide[Container.text_service])
):
    text_dict = text.dict()

    # TODO: what if admin wants to have its own private text?
    # only texts added by admin can be publicly available
    text_dict["is_public"] = False if UserRole(request.user_role) < UserRole.admin else True

    text_dict["added_by"] = request.user_id
    text_db = TextDb(**text_dict)

    await text_service.insert_text(
        text=text_db,
        user_id=request.user_id,
        role=UserRole(request.user_role)
    )


@router.get(
    "/",
    dependencies=[Depends(optional_authentication)],
    response_model=list[TextDetail]
)
@inject
async def get_texts(
        request: Request,
        pagination: Pagination = Depends(),
        text_service: TextService = Depends(Provide[Container.text_service])
):
    user_id = getattr(request, "user_id", None)

    if user_id is None:  # user is not authenticated -> return all publicly available texts
        return await text_service.get_public_texts(pagination=pagination)

    else:
        return await text_service.get_user_texts(user_id=request.user_id, pagination=pagination)


@router.get(
    "/{text_id}",
    dependencies=[Depends(optional_authentication)],
    response_model=TextOut
)
@inject
async def get_text(
        text_id: UUID4,
        request: Request,
        text_service: TextService = Depends(Provide[Container.text_service])
):
    user_id = getattr(request, "user_id", None)
    text = await text_service.get_text(text_id=text_id, user_id=user_id)
    return text


@router.delete(
    "/{text_id}",
    dependencies=[Depends(required_authentication)]
)
@inject
async def delete_text(
        text_id: UUID4,
        request: Request,
        text_service: TextService = Depends(Provide[Container.text_service]),
):
    await text_service.delete_text(
        text_id=text_id,
        user_id=request.user_id,
        user_role=UserRole(request.user_role)
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
