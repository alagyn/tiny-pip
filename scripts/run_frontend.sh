#!/bin/bash
set -e

home=$(realpath $(dirname $0)/..)
cd $home/frontend/tiny-pip
npm run dev

