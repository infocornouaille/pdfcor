# Contributing to pdfcor

Contributions are welcome! Feel free to open an issue or submit a pull request on our GitHub repository.

## Development Setup

We use `uv` for managing virtual environments and dependencies during development.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/infocornouaille/pdfcor.git # Replace with actual repo URL if different
    cd pdfcor
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    # Install uv if you haven't already: https://github.com/astral-sh/uv#installation
    uv venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies (including development tools like Ruff)**:
    ```bash
    uv pip install -e .[dev]
    ```
This installs the package in editable mode (`-e`) along with the `dev` optional dependencies specified in `pyproject.toml`.

## Code Style and Quality

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and code formatting (Black-compatible style).
After setting up your development environment, you can format and check your code by running:

```bash
# Format the code
ruff format .

# Check for linting issues (and autofix some)
ruff check --fix .
```

A GitHub Actions workflow is also in place to automatically check code formatting and linting on pushes and pull requests.
Please ensure your contributions pass these checks.

## Running Tests

To run the unit tests:
```bash
python -m unittest discover tests
```
Or, if your virtual environment is active:
```bash
unittest discover tests
```
Ensure all tests pass before submitting contributions.

## Building and Publishing

This project uses [Hatchling](https://hatch.pypa.io/latest/) as its build backend, as defined in `pyproject.toml`.

### Building the Package

1.  Ensure you have the `build` package installed:
    ```bash
    uv pip install build  # Or: python -m pip install build
    ```
2.  Run the build command from the project root:
    ```bash
    python -m build
    ```
    This will create `sdist` and `wheel` files in the `dist/` directory.

### Publishing to PyPI (Locally)

Publishing is typically done by project maintainers.

1.  Ensure you have `twine` installed:
    ```bash
    uv pip install twine  # Or: python -m pip install twine
    ```
2.  Upload the distributions from the `dist/` directory:
    ```bash
    twine upload dist/*
    ```
    You will be prompted for your PyPI username and password. It's recommended to use API tokens with Twine.

## License

This project is licensed under the MIT License. See the `LICENSE` file in the root of the repository for more details.
