#!/bin/bash
set -e
# cd to self bash script directory
cd "${BASH_SOURCE[0]%/*}"

echo Fixing code style with black
black src tests test_install

echo Running flake8
flake8 src tests test_install
echo Running pylint
pylint src tests test_install
echo Running mypy
mypy src tests test_install
echo Linting complete!