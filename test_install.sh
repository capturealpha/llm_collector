#!/bin/bash

# Exit if any command fails
set -e

# Define package name for uninstallation
PACKAGE_NAME="llm_collector"

# Clean up previous build artifacts
rm -rf build/ dist/ *.egg-info

# Build the package
echo "Building the package..."
python3 setup.py sdist bdist_wheel

# Install the package using the wheel file
echo "Installing the package locally..."
pip3 install dist/*.whl

# Run the package (optional)
echo "Running the package..."
llm_collector [option]

#Uninstall the package (optional)
echo "Uninstalling the package..."
pip3 uninstall -y $PACKAGE_NAME

echo "Local installation test complete."
