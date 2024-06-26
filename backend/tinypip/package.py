import enum
import os
from typing import List, Dict, Any, Optional
import re


class RelType(enum.IntEnum):
    UNKNOWN = enum.auto()
    SRC = enum.auto()
    WHL = enum.auto()


def normalizeToWheel(pkgName: str) -> str:
    return re.sub(r"[-_.]+", "_", pkgName).lower()


def normalizeName(pkgName: str) -> str:
    return re.sub(r"[-_.]+", "-", pkgName).lower()


VERSION_RE = re.compile(
    r'([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$'
)


def isVersionCanonical(version):
    return VERSION_RE.fullmatch(version) is not None


class Release:

    def __init__(
        self,
        package: str,
        filepath: str,
        version: str,
        instType: Optional[RelType] = None,
        sha256: Optional[str] = None
    ) -> None:
        self.package = package
        self.filepath = filepath
        self.version = version
        self.instType = instType
        self.sha256 = sha256

    def toDict(self) -> Dict[str, Any]:
        fname = os.path.split(self.filepath)[1]
        out: Dict[str, Any] = {
            "filename": fname,
            "url": fname
        }

        if self.sha256 is not None:
            out["hashes"] = {
                "sha256": self.sha256
            }

        return out


def getType(filepath: str) -> RelType:
    ext = os.path.splitext(filepath)[1]
    if ext == '.gz':
        return RelType.SRC
    elif ext == '.whl':
        return RelType.WHL
    else:
        return RelType.UNKNOWN


def releaseFromFilename(filename: str) -> Release:
    instType = getType(filename)
    if instType == RelType.SRC:
        # source distro
        return _makeSourceDistro(filename)

    elif instType == RelType.WHL:
        # wheel
        return _makeWheel(filename)
    else:
        raise RuntimeError("Unknown filetype")


TGZ_LEN = len(".tar.gz")


def _makeSourceDistro(filename: str) -> Release:
    # get just the name
    namestr = os.path.split(filename)[1]
    # pull off the ext
    namestr = namestr[:-TGZ_LEN]
    # try to pull off the version
    m = VERSION_RE.search(namestr)
    if m is None:
        raise RuntimeError("Cannot find Source Distro Version")

    version = m.group()
    package = normalizeName(namestr[:-len(version) - 1])

    return Release(
        package=package,
        version=version,
        filepath=os.path.join(package, filename),
        instType=RelType.SRC
    )


def _makeWheel(filename: str) -> Release:
    # pull off the ext
    namestr = os.path.splitext(filename)[0]
    # split into components
    name, version, pyTag, abiTag, platform = namestr.split("-")

    package = normalizeName(name)

    return Release(
        package=package,
        version=version,
        filepath=os.path.join(package, filename),
        instType=RelType.WHL
    )


class Package:

    def __init__(self, name: str) -> None:
        self.name = name
        self.releases: List[Release] = []

    def addRelease(self, inst: Release):
        self.releases.append(inst)
        # TODO error check for dupes?
