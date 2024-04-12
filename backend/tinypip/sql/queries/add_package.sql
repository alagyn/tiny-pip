INSERT INTO packages
(pkg_name)
VALUES ( :pkg_name )
ON CONFLICT DO NOTHING
RETURNING pkg_id