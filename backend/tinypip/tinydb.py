import sqlite3
import os
from tinypip.config import config
from typing import Optional
import hashlib

from tinypip.package import Package, InstType, Instance, getType, isVersionCanonical, normalizeToWheel

SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")


def _loadStatement(*path: str) -> str:
    with open(os.path.join(SQL_DIR, *path), mode='r') as f:
        return f.read()


ADD_PKG_STMT = _loadStatement("queries", "add_package.sql")
ADD_INST_STMT = _loadStatement("queries", "add_instance.sql")
GET_INSTS_STMT = _loadStatement("queries", "get_instances.sql")


def autocommit(func):

    def wrapper(self: 'TinyDB', *args, **kwargs):
        func(self, *args, **kwargs)
        self.con.commit()

    return wrapper


class TinyDB:

    def __init__(self) -> None:
        needsInit = not os.path.isfile(config.index_db)
        print(f"TinyDB.init() Connecting to {config.index_db}")
        if sqlite3.threadsafety != 3:
            raise RuntimeError("sqlite3 not thread safety is not serialized")
        self.con = sqlite3.connect(config.index_db, check_same_thread=False)

        if needsInit:
            print(f"TinyDB.init() Initializing Schemas")
            cur = self.con.cursor()
            cur.execute(_loadStatement("schemas", "packages_schema.sql"))
            cur.execute(_loadStatement("schemas", "instance_schema.sql"))
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
                self._addInstance(name, pkgID, instPath)

    def _insertPackage(self, packageName: str) -> int:
        """
        Attempt to add a new package. Does nothing if
        package with passed name already exists.
        Returns (new) package ID
        """

        res = self.con.execute(ADD_PKG_STMT, {
            "pkg_name": packageName
        })
        out = int(res.fetchone()[0])

        return out

    def _addInstance(self, pkgName: str, pkgID: int, filepath: str):
        namestr = os.path.split(filepath)[1]
        namestr = os.path.splitext(namestr)[0]
        instType = getType(filepath)
        if instType == InstType.SRC:
            # source distro
            self._addSourceDistro(
                pkgName=pkgName,
                pkgID=pkgID,
                filepath=filepath,
                namestr=namestr
            )
        elif instType == InstType.WHL:
            # wheel
            self._addWheel(
                pkgName=pkgName,
                pkgID=pkgID,
                filepath=filepath,
                namestr=namestr
            )
        else:
            # TODO error
            pass

    def _addSourceDistro(
        self, pkgName: str, pkgID: int, filepath: str, namestr: str
    ):
        # get rid of .tar
        namestr = os.path.splitext(namestr)[0]
        if not namestr.startswith(pkgName):
            print(f"Bad instance of package '{pkgName}': '{filepath}'")
            # TODO error
            return

        # +1 for the dash after the name
        versionStr = namestr[len(pkgName) + 1:]
        if not isVersionCanonical(versionStr):
            print(f"Bad instance version of package '{pkgName}': '{filepath}'")
            # TODO error
            return

        self._insertInstance(
            pkgID=pkgID, pkgVersion=versionStr, pkgPath=filepath
        )

    def _addWheel(self, pkgName: str, pkgID: int, filepath: str, namestr: str):
        wheelNormName = normalizeToWheel(pkgName)

        name, version, pyTag, abiTag, platform = namestr.split("-")

        if name != wheelNormName:
            print(f"Bad instance of package '{pkgName}': '{filepath}'")
            # TODO error
            return

        if not isVersionCanonical(version):
            print(f"Bad instance version of package '{pkgName}': '{filepath}'")
            # TODO error
            return

        self._insertInstance(pkgID=pkgID, pkgVersion=version, pkgPath=filepath)

    def _insertInstance(self, pkgID: int, pkgVersion: str, pkgPath: str):
        h = hashlib.sha256()
        BUFSIZE = 65536
        with open(os.path.join(config.pkg_base, pkgPath), mode='rb') as f:
            while True:
                data = f.read(BUFSIZE)
                if not data:
                    break
                h.update(data)
        self.con.execute(
            ADD_INST_STMT,
            {
                "pkg_id": pkgID,
                "pkg_version": pkgVersion,
                "pkg_path": pkgPath,
                "sha256": h.hexdigest()
            }
        )

    @autocommit
    def addPackage(self, packageName: str) -> int:
        return self._insertPackage(packageName)

    def getPackage(self, packageName: str) -> Optional[Package]:
        res = self.con.execute(GET_INSTS_STMT, {
            "pkg_name": packageName
        })

        pkg = Package(packageName)

        for x in res.fetchall():
            inst = Instance(*x)
            pkg.addInstance(inst)

        if len(pkg.instances) == 0:
            return None

        return pkg


database = TinyDB()
