import enum
import os
from typing import List, Dict, Any
import re


class InstType(enum.IntEnum):
    UNKNOWN = enum.auto()
    SRC = enum.auto()
    WHL = enum.auto()


def getType(filepath: str) -> InstType:
    ext = os.path.splitext(filepath)[1]
    if ext == '.gz':
        return InstType.SRC
    elif ext == '.whl':
        return InstType.WHL
    else:
        return InstType.UNKNOWN


def normalizeToWheel(pkgName: str) -> str:
    return re.sub(r"[-_.]+", "_", pkgName).lower()


def normalizeName(pkgName: str) -> str:
    return re.sub(r"[-_.]+", "-", pkgName).lower()


def isVersionCanonical(version):
    return re.match(
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$',
        version
    ) is not None


class Instance:

    def __init__(self, filepath: str, version: str, sha256: str) -> None:
        self.filepath = filepath
        self.version = version

        self.instType = getType(filepath)

        self.sha256 = sha256

    def toDict(self) -> Dict[str, Any]:
        fname = os.path.split(self.filepath)[1]
        out = {
            "filename": fname,
            "url": fname,
            "hashes": {
                "sha256": self.sha256
            }
        }

        return out


class Package:

    def __init__(self, name: str) -> None:
        self.name = name
        self.instances: List[Instance] = []

    def addInstance(self, inst: Instance):
        self.instances.append(inst)
        # TODO error check for dupes?
