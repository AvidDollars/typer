from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.requests import Request
from pydantic import UUID4

from ..containers import Container
from ..models.typing_session import TypingSessionIn, TypingSessionDb, TypingSessionOut
from ..services.auth_service import required_authentication
from ..services.typing_session_service import TypingSessionService

router = APIRouter(
    prefix="/typing-sessions",
    tags=["Typing Session"],
    dependencies=[Depends(required_authentication)],
)


@router.post("", status_code=status.HTTP_201_CREATED)
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


@router.get("", response_model=list[TypingSessionOut])
@inject
async def get_user_typing_sessions(
        request: Request,
        typing_session_service: TypingSessionService = Depends(Provide[Container.typing_session_service]),

        # if "?text=<text_id>" query parameter is not provided -> all user's typing sessions will be returned
        text: UUID4 = None
):
    return await typing_session_service.get_user_typing_sessions(user_id=request.user_id, text_id=text)
