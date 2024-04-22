#!/bin/bash
set -e

home=$(realpath $(dirname $0)/..)
cd $home/frontend/
npm run dev

