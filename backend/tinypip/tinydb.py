import sqlite3
import os
from tinypip.config import config
from typing import Optional, List
import hashlib

from tinypip.package import Package, RelType, Release, releaseFromFilename, getType

SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")


def _loadStatement(*path: str) -> str:
    with open(os.path.join(SQL_DIR, *path), mode='r') as f:
        return f.read()


ADD_PKG_STMT = _loadStatement("queries", "add_package.sql")
GET_PKG_ID_STMT = _loadStatement("queries", "get_package_id.sql")
ADD_INST_STMT = _loadStatement("queries", "add_release.sql")
GET_INSTS_STMT = _loadStatement("queries", "get_releases.sql")
GET_PROJECTS_STMT = _loadStatement("queries", "get_projects.sql")
SEARCH_INST_STMT = _loadStatement("queries", "search_release.sql")


def autocommit(func):

    def wrapper(self: 'TinyDB', *args, **kwargs):
        out = func(self, *args, **kwargs)
        self.con.commit()
        return out

    return wrapper


class TinyDB:

    def __init__(self) -> None:
        needsInit = not os.path.isfile(config.index_db)
        print(f"TinyDB.init() Connecting to {config.index_db}")
        if sqlite3.threadsafety != 3:
            raise RuntimeError(
                "sqlite3 version does not support serialized multithreading"
            )
        self.con = sqlite3.connect(config.index_db, check_same_thread=False)

        if needsInit:
            print(f"TinyDB.init() Initializing Schemas")
            cur = self.con.cursor()
            cur.execute(_loadStatement("schemas", "packages_schema.sql"))
            cur.execute(_loadStatement("schemas", "release_schema.sql"))
            self.con.commit()

            self.reindex()

    @autocommit
    def reindex(self):
        """
        Scan packages and update DB
        """
        print(f'TinyDB.reindex() Indexing')
        for name in os.listdir(config.pkg_base):
            pkgPath = os.path.join(config.pkg_base, name)
            if not os.path.isdir(pkgPath):
                print(
                    f"TinyDB.reindex() Found non-directory in pkg_base: '{pkgPath}'"
                )
                continue
            pkgID = self._insertPackage(name)
            # TODO attempt to load metadata?
            for instName in os.listdir(pkgPath):
                instPath = os.path.join(name, instName)
                try:
                    release = releaseFromFilename(instName)
                except Exception as err:
                    print(f"Bad release of package '{name}': {err}")
                    continue

                if release.filepath != instPath:
                    print(
                        f"Bad release of package '{name}': '{instPath}', package name doesn't match"
                    )
                    continue
                self._addRelease(release, pkgID)

    @autocommit
    def addRelease(self, inst: Release):
        pkgID = self.addPackage(inst.package)
        self._addRelease(inst, pkgID)

    @autocommit
    def addPackage(self, packageName: str) -> int:
        """
        Attempt to add a new package. Does nothing if
        package with passed name already exists.
        Returns (new) package ID
        """
        return self._insertPackage(packageName)

    def _insertPackage(self, packageName: str) -> int:
        res = self.con.execute(ADD_PKG_STMT, {
            "pkg_name": packageName
        })
        data = res.fetchone()

        out = int(data[0])

        return out

    def _addRelease(self, inst: Release, pkgID: int):
        if inst.sha256 is None:
            h = hashlib.sha256()
            BUFSIZE = 65536
            with open(os.path.join(config.pkg_base, inst.filepath),
                      mode='rb') as f:
                while True:
                    data = f.read(BUFSIZE)
                    if not data:
                        break
                    h.update(data)
            inst.sha256 = h.hexdigest()

        self.con.execute(
            ADD_INST_STMT,
            {
                "pkg_id": pkgID,
                "pkg_version": inst.version,
                "pkg_path": inst.filepath,
                "sha256": inst.sha256
            }
        )

    def getPackage(self, packageName: str) -> Optional[Package]:
        res = self.con.execute(GET_INSTS_STMT, {
            "pkg_name": packageName
        })

        pkg = Package(packageName)

        for x in res.fetchall():
            path = x[0]
            version = x[1]
            sha256 = x[2]
            inst = Release(packageName, path, version, getType(path), sha256)
            pkg.addRelease(inst)

        if len(pkg.releases) == 0:
            return None

        return pkg

    def getProjects(self) -> List[str]:
        res = self.con.execute(GET_PROJECTS_STMT)
        return list(res.fetchall())


database = TinyDB()
