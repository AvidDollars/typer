from fastapi import APIRouter

from . import activate, login, register, text
from ..utils import register_routes

router = APIRouter()

register_routes(
    router,
    register.router, activate.router, login.router, text.router
)

__all__ = (router, )
