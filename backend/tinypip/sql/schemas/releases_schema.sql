CREATE TABLE IF NOT EXISTS releases
(
    pkg_id INTEGER NOT NULL,
    pkg_version TEXT,
    pkg_path TEXT,
    sha256 TEXT,
    FOREIGN KEY(pkg_id) REFERENCES packages(pkg_id)
)