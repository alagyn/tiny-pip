#!/bin/bash
set -e

home=$(realpath $(dirname $0)/..)
cd $home

dataDir=test-data

# clear existing data
rm -rf $dataDir
mkdir $dataDir

# copy the config file
cp docs/example-config.yaml $dataDir/config.yaml

# create package dir
packageDir=$dataDir/packages
mkdir $packageDir
cd $packageDir

# download some test packages
mkdir diamondpack
cd diamondpack
wget https://files.pythonhosted.org/packages/ce/06/bd7e5305e68a1d1a22ca37f07eb1b970c9ada3de9643f1f093c78702cc8e/diamondpack-1.4.5-py3-none-any.whl
wget https://files.pythonhosted.org/packages/1e/fc/422a5202902e9c2449dd508293848b4867b2b2452ba28272d5684319e4dc/diamondpack-1.4.5.tar.gz

cd ..

mkdir py-imgui-redux
cd py-imgui-redux
wget https://files.pythonhosted.org/packages/3a/8e/08cf3f80fd79cb319b22f5a57ea44346008dbd3be1e43b6a24705db8c51d/py_imgui_redux-2.2.0.tar.gz
wget https://files.pythonhosted.org/packages/48/28/8c2b314e531fb9fff39ad889ee87430d7c964741a69280e4ca91c8f92b76/py_imgui_redux-2.2.0-cp312-cp312-win_amd64.whl
wget https://files.pythonhosted.org/packages/d2/ae/5b6f6bb4e7ebfdd56924e2618016bd33ceb12c494236d457ed87ed1f467b/py_imgui_redux-2.2.0-cp312-cp312-manylinux_2_28_x86_64.whl

