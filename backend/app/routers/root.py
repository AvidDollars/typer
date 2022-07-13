from fastapi import APIRouter

router = APIRouter(
    prefix="", tags=["Root"]
)


@router.get("/")
async def get_root():
    return {"message": "root page"}
