from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, status
from fastapi.requests import Request

from ..containers import Container
from ..models.enums import UserRole
from ..models.text import TextIn, TextDb
from ..services import TextService
from ..services.auth_service import CustomHttpBearer

router = APIRouter(
    prefix="/text", tags=["Text"]
)


@router.post(
    "/",
    dependencies=[Depends(CustomHttpBearer())],
    status_code=status.HTTP_201_CREATED
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
    await text_service.insert_text(text_db)
