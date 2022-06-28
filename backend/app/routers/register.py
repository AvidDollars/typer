from fastapi import APIRouter, Depends
from ..services import AbstractEmailService
from dependency_injector.wiring import inject, Provide
from ..containers import Container

router = APIRouter(
    prefix="/register",
)


@router.get("/")
@inject
async def register_user(
        email_service: AbstractEmailService = Depends(Provide[Container.email_service])
):
    await email_service.simple_send()
