from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from ..containers import Container
from ..models import UserIn
from ..services import UserRegistrationEmailService, UserService

router = APIRouter(
    prefix="/register", tags=["User"]
)


@router.post("/")
@inject
async def register_user(
        user: UserIn,
        user_service: UserService = Depends(Provide[Container.user_service]),
        email_service: UserRegistrationEmailService = Depends(Provide[Container.user_registration_email_service]),
):

    # activation_token is returned if unique constraint is not violated (name, email)
    activation_token = await user_service.register_user(user)

    await email_service.registration_email(recipient=user.email, activation_token=activation_token)  # noqa
    return {"message": "email sent"}
