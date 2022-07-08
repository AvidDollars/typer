from fastapi import APIRouter

from . import activate, login, register, text, typing_session, text_rating
from ..utils import register_routes

router = APIRouter()

register_routes(
    router,

    # endpoints
    register.router,
    activate.router,
    login.router,
    text.router,
    typing_session.router,
    text_rating.router
)

__all__ = (router, )
