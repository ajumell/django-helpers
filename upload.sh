#!/bin/sh

echo "Cleaning up previous build data"
rm -rf dist
rm MANIFEST

python setup.py sdist upload

echo "Cleaning up current build data"
rm -rf dist
rm MANIFEST
