from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.requests import Request

from ..models.typing_session import TypingSessionIn, TypingSessionDb
from ..services.auth_service import required_authentication
from ..services.typing_session_service import TypingSessionService
from ..containers import Container

router = APIRouter(
    prefix="/typing-sessions", tags=["Typing Session"]
)


@router.post(
    "/",
    dependencies=[Depends(required_authentication)],
    status_code=status.HTTP_201_CREATED,

)
@inject
async def add_typing_session(
        request: Request,
        session: TypingSessionIn,
        typing_session_service: TypingSessionService = Depends(Provide[Container.typing_session_service])
):
    typing_session_dict = session.dict()
    typing_session_dict.update(user_id=request.user_id)
    typing_session_db = TypingSessionDb(**typing_session_dict)

    await typing_session_service.insert_typing_session(typing_session_db)
