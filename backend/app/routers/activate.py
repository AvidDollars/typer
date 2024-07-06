from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from containers import Container
from services import UserService

router = APIRouter(
    prefix="/activate", tags=["User"]
)


@router.get("/{activation_token}")
@inject
async def activate_user(
        activation_token: str,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    result = await user_service.activate_user(activation_token)
    return result
