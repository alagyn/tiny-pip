# tiny-pip
A minimal service for hosting a local PyPi index.

## Features
TODO lol

## Config
Tinypip requires but a single yaml file for configuration

```yaml
tinypip:
  # root directory for stored packages
  pkg_base: test-data/packages
  # path to sqlite package database
  index_db: test-data/index.db
  # OPTIONAL fallthrough URL if a package is not found locally
  # remove this key to disable fallthrough
  fallthrough: "https://www.pypi.org/simple"
```
