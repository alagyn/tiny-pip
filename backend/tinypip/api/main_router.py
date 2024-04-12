from fastapi import APIRouter

from . import index

router = APIRouter(prefix="/api")

router.include_router(index.router)
