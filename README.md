# llm_collector

`llm_collector` is a Python package that collects file information from a Django project, including Python, HTML, and CSS files. It generates `.jsonl` files containing metadata about the files, such as the number of tokens and file size.

## Installation

To install `llm_collector`, run the following command:

bash pip install llm-collector
Or, if you are using Poetry:
Replit

bash poetry add llm-collector
## Usage

After installing, you can run the script with the following command:
Replit

bash llm_collector [option]
Replace `[option]` with one of the available options to specify which files to collect.

## Available Options

- `django-all`: Collects all relevant Django files.
- `django-html`: Collects only HTML-related files.
- `django-views`: Collects only files related to Django views.
- `django-base`: Collects base files.
- `django-root`: Collects files from the root directory.

## Testing Locally

To test the `llm_collector` package locally after making changes, you can build and install it using the following script:
Replit

bash #!/bin/bash

Exit if any command fails

set -e

Define package name for uninstallation

PACKAGE_NAME="llm_collector"

Clean up previous build artifacts

rm -rf build/ dist/ *.egg-info

Build the package

echo "Building the package..." python3 setup.py sdist bdist_wheel

Install the package using the wheel file

echo "Installing the package locally..." pip3 install dist/*.whl

Run the package (optional)

echo "Running the package..." llm_collector [option]

Uninstall the package (optional)

echo "Uninstalling the package..." pip3 uninstall -y $PACKAGE_NAME

echo "Local installation test complete."
Make sure to replace `[option]` with the actual option you want to test. This script will build the package, install it locally, optionally run it, and then uninstall it.

## Contributing

Contributions to `llm_collector` are welcome. Please ensure that your code adheres to the existing style and that all tests pass.

## License

`llm_collector` is released under the MIT License. See the LICENSE file for more details.
