#!/bin/bash

# Exit in case of error
set -e

# Define package name and version
PACKAGE_NAME="llm_collector"
PACKAGE_VERSION="0.1.0"
rm -rf build/ dist/ *.egg-info
echo "Installing setuptools and wheel..."
pip3 install setuptools wheel
echo "Building the package..."
python3 setup.py sdist bdist_wheel
if ! command -v twine &> /dev/null
then
    echo "Installing twine..."
    pip3 install twine
fi
pip3 install --force-reinstall dist/*.whl
echo "Running the package..."
llm_collector [option]
echo "Uninstalling the package..."
pip3 uninstall -y $PACKAGE_NAME
echo "Local installation test complete."


## Upload the package to PyPI
#echo "Uploading the package to PyPI..."
#twine upload dist/*

echo "Package $PACKAGE_NAME version $PACKAGE_VERSION has been published to PyPI."
