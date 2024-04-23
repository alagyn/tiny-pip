#!/bin/bash
set -e

home=$(realpath $(dirname $0))
cd $home
npm run dev

