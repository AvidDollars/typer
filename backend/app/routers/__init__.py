from fastapi import APIRouter
from . import register
from . import activate

router = APIRouter()
router.include_router(register.router)
router.include_router(activate.router)

__all__ = (router, )
