from fastapi import APIRouter

router = APIRouter(
    prefix="/register"
)


@router.get("/")
async def register_user():
    ...
