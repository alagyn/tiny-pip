SELECT i.pkg_path, i.pkg_version, i.sha256 FROM instances AS i
INNER JOIN packages AS p ON p.pkg_id = i.pkg_id
WHERE p.pkg_name = :pkg_name