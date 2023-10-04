# Python Fortress

Python Fortress is a library designed to facilitate interaction with an API to retrieve an .env file and load its values into your environment variables. It's designed for securely and efficiently loading environment variables from a remote source.

[![codecov](https://codecov.io/gh/magestree/python_fortress/branch/develop/graph/badge.svg)](https://codecov.io/gh/magestree/python_fortress)

## Features

- Easy loading and configuration.
- Secure retrieval of the `.env` file content from [passfortress.com](https://www.passfortress.com) API.
- Simple and efficient usage with intuitive methods.

## Installation

To install the project dependencies, run:

```bash
pip install -r requirements.txt
```

## Basic usage

The main module `fortress.py` provides the `Fortress` class and a convenience function `configure()` and `load_env()`.
You just need configure your `Fortress` instance and then, call the `load_env()` method with desired envfile `id`.

## Example:

```python
from python_fortress.fortress import Fortress

credentials = {
    "api_key": "<YOUR_API_KEY>",
    "access_token": "<YOUR_ACCESS_TOKEN>",
    "master_key": "<YOUR_MASTER_KEY>"
}

fortress = Fortress()
fortress.configure(**credentials)
fortress.load_env(envfile_id="<YOUR_ENVFILE_ID>")
```

## Tests
The project comes with a set of tests to ensure everything works as expected. You can run the tests using pytest:

```bash
pip install -r requirements_dev.txt
pytest
```

To obtain a coverage report:
```bash
coverage run -m pytest
coverage report
```

## CI/CD
Thanks to GitHub Actions, each push or pull request will trigger the CI pipeline which will run tests and calculate code coverage.


## Contribution
If you're interested in contributing to the project, please follow these steps:

1. Fork repository.
2. Create a new branch for your feature or fix.
3. Implement your change or fix.
4. Run the tests to make sure everything is working as expected.
5. Open a pull request.


## Licencia
MIT
