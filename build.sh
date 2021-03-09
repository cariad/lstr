#!/bin/bash -e
echo "${1:?}" > lstr/VERSION
rm -rf dist
python setup.py bdist_wheel
rm -rf build
