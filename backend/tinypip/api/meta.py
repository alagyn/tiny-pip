from fastapi import APIRouter

router = APIRouter(prefix="metadata", tags=["UI"])


@router.get("/")
async def get_metadata():
    pass
