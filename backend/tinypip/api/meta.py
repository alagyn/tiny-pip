from fastapi import APIRouter

from tinypip.tinydb import database

router = APIRouter(prefix="/metadata", tags=["UI"])


@router.get("/")
async def get_metadata():
    return {
        "indexURL": "http://localhost:8000/",  # TODO config
        "numPackages": database.countPackages(),
        "numReleases": database.countReleases()
    }
