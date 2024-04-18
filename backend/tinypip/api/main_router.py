from fastapi import APIRouter

from . import index
from . import meta

router = APIRouter(prefix="/api")

router.include_router(index.router)
router.include_router(meta.router)
