#!/bin/bash

home=$(realpath $(dirname $))
cd $home

export TINYPIP_CONFIG=test-data/tinypip.yaml

rm test-data/index.db

./venv/bin/python -m tinypip