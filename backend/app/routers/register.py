from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from ..containers import Container
from ..models.user import UserIn
from ..services import AbstractEmailService, AbstractHashingService


router = APIRouter(
    prefix="/register",
)


@router.post("/")
@inject
async def register_user(
        user: UserIn,
        email_service: AbstractEmailService = Depends(Provide[Container.user_registration_email_service]),
        hashing_service: AbstractHashingService = Depends(Provide[Container.hashing_service])
):
    ...
    #await email_service.simple_send(recipient=user.email)
