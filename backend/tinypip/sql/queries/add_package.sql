INSERT INTO packages
(pkg_name)
VALUES ( :pkg_name )
ON CONFLICT DO UPDATE SET pkg_name = pkg_name
RETURNING pkg_id