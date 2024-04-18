from fastapi import APIRouter, UploadFile, File, Request, Form
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from pydantic import BaseModel
import os
from typing import Annotated

from tinypip.tinydb import database
from tinypip.config import config
from tinypip.package import Release, releaseFromFilename

router = APIRouter(prefix="/index", tags=["packages"])


@router.get("/", response_class=JSONResponse)
async def get_projects():
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


@router.get("/{pkg_name}/", response_class=JSONResponse)
async def get_package(pkg_name: str):
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
                          for x in pkg.releases}),
        "files": [x.toDict() for x in pkg.releases]
    }

    return JSONResponse(
        content=data, media_type="application/vnd.pypi.simple.v1+json"
    )


@router.get("/{pkg_name}/{filepath}", response_class=FileResponse)
async def download_file(pkg_name: str, filepath: str):
    fullpath = os.path.join(config.pkg_base, pkg_name, filepath)
    return FileResponse(fullpath)


@router.post("/")
async def upload_file(
    name: Annotated[str, Form()],
    version: Annotated[str, Form()],
    content: Annotated[UploadFile, File()]
):
    if content.filename is None:
        raise RuntimeError()
    filepath = os.path.join(name, content.filename)

    release = Release(name, filepath, version)

    fullpath = os.path.join(config.pkg_base, release.filepath)

    if os.path.exists(fullpath) and not config.overwrite:
        return JSONResponse(
            {
                "message": "Cannot overwrite exising file"
            }, status_code=403
        )

    BUFSIZE = 65535
    with open(fullpath, mode='wb') as f:
        while True:
            data = await content.read(BUFSIZE)
            if not data:
                break
            f.write(data)

    database.addRelease(release)
