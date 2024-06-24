#!/bin/bash
set -e

home=$(realpath $(dirname $0))
cd $home
root=$(realpath $home/..)


export TINYPIP_CONFIG=$root/test-data/config.yaml

$root/venv/bin/python -m tinypip