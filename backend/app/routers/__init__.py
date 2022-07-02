from fastapi import APIRouter
from . import register
from . import activate
from . import login

router = APIRouter()
router.include_router(register.router)
router.include_router(activate.router)
router.include_router(login.router)

__all__ = (router, )
