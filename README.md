README.md:
# llm-collector

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

## Contributing

Contributions to `llm_collector` are welcome. Please ensure that your code adheres to the existing style and that all tests pass.

## License

`llm_collector` is released under the MIT License. See the LICENSE file for more details.
