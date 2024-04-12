from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from pydantic import BaseModel
import os

from tinypip.tinydb import database
from tinypip.config import config

router = APIRouter(prefix="/index", tags=["packages"])


@router.get("/")
def get_projects():
    projects = database.getProjects()
    data = {
        "meta": {
            "api-version": "1.0"
        },
        "projects": [{
            "name": x
        } for x in projects]
    }
    return JSONResponse(content=data)


@router.get("/{pkg_name}/")
def get_package(pkg_name: str):

    pkg = database.getPackage(pkg_name)

    if pkg is None:
        if config.fallthrough:
            return RedirectResponse(config.ft_url + pkg_name)
        else:
            return JSONResponse(
                {
                    "message": "Package Missing"
                }, status_code=404
            )

    data = {
        "meta": {
            "api-version": "1.0"
        },
        "name": pkg_name,
        "versions": list({x.version
                          for x in pkg.instances}),
        "files": [x.toDict() for x in pkg.instances]
    }

    return JSONResponse(
        content=data, media_type="application/vnd.pypi.simple.v1+json"
    )


@router.get("/{pkg_name}/{filepath}")
def download_file(pkg_name: str, filepath: str):
    fullpath = os.path.join(config.pkg_base, pkg_name, filepath)

    return FileResponse(fullpath)
