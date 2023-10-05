#!/bin/sh

git fetch --prune
echo "Go to folder"
cd pollination_dash_io
echo "Building distribution"
python setup.py sdist bdist_wheel
echo "Pushing new version to PyPi"
twine upload dist/* -u $PYPI_USERNAME -p $PYPI_PASSWORD
