from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, HTTPException, status

from ..containers import Container
from ..models.user import UserLogin
from ..services import UserService

router = APIRouter(
    prefix="/login", tags=["Auth"]
)


@router.post("/")
@inject
async def login_user(
        user: UserLogin,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    missing_name_and_mail = user.name is None and user.email is None
    missing_password = user.password is None

    if missing_name_and_mail or missing_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="password along with email or name must be provided"
        )

    token = await user_service.login_user(user)
    return {"token": token}
