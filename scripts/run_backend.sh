#!/bin/bash
set -e

home=$(realpath $(dirname $0)/..)
cd $home

export TINYPIP_CONFIG=$home/test-data/config.yaml

cd backend
$home/venv/bin/python -m tinypip