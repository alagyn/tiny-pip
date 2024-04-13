# tiny-pip
A minimal service for hosting a local PyPi index.
tiny-pip conforms to the [Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/#json-serialization)

## Features
- Minimal configuration
- Fallthrough to external python indicies

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
  # enable to allow overwriting existing package versions
  overwrite: true
```
