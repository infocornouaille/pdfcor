# pdfcor

![PyPI version](https://img.shields.io/pypi/v/pdfcor.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pdfcor.svg)
[![Documentation](https://img.shields.io/badge/docs-online-blue?style=flat-square)](https://infocornouaille.github.io/pdfcor/)

pdfcor is a versatile Python package for working with PDF files. It allows you to extract content in Markdown format with images, merge PDFs, and extract individual pages.

For detailed documentation, please visit our [GitHub Pages site](https://infocornouaille.github.io/pdfcor/).

## Installation

```
pip install pdfcor
```

### Using pipx (Recommended for CLI tool)

If you want to use `pdfcor` as a command-line tool, `pipx` is recommended as it installs the package in an isolated environment and makes its entry points available system-wide.

First, ensure `pipx` is installed:
```
python -m pip install --user pipx
python -m pipx ensurepath
```

Then, install `pdfcor` using `pipx`:
```
pipx install pdfcor
```
Now you can run `pdfcor` commands directly from your terminal. To upgrade later: `pipx upgrade pdfcor`.

### Using uv (Alternative Installer)

If you prefer using `uv` (a fast Python package installer), you can install `pdfcor` with:
```
uv pip install pdfcor
```
This is an alternative to using `pip`.

## Dependencies

pdfcor depends on the following libraries:

- PyMuPDF (fitz): for extracting content from PDFs and manipulating PDF files
- Pillow (PIL): for image processing

These dependencies will be automatically installed when you install pdfcor via pip.

## Usage

pdfcor can be used from the command line with various options:

### Extracting Content to Markdown

```
pdfcor process [OPTIONS]
```
(Or more explicitly: `pdfcor process --input-folder <input_folder> --output-folder <output_folder> [--recursive] [--resize]`)

#### Options

- `--input-folder`: Specifies the input folder containing the PDF files to process. By default, it uses the current directory.
- `--output-folder`: Defines the output folder for the Markdown files and extracted images. If not specified, it uses a subfolder named `pdfcor_output` within the input folder.
- `--recursive`: Enables recursive processing of subfolders.
- `--resize`: Resizes extracted images to fit on an A4 page.

### Merging PDFs

```
pdfcor merge [OPTIONS]
```
(Or more explicitly: `pdfcor merge --input-folder <input_folder> --output-file <output_filename_or_path>`)

This command merges all PDFs in a folder without any transformation.

#### Options

- `--input-folder`: Specifies the folder containing the PDFs to merge. By default, uses the current directory.
- `--output-file`: Specifies the name and/or path of the merged PDF file.
    - If only a name is provided (e.g., `my_file.pdf`), the merged PDF will be saved in the input folder (`--input-folder`).
    - If a full path is provided (e.g., `/another/folder/my_file.pdf`), it will be saved to that location.
    - If this option is not used, the merged file will be named after the input folder (e.g., `input_folder_name.pdf`) and saved in that same input folder.

### Extracting Pages

```
pdfcor extract <pdf_file>
```

This command extracts all pages from a PDF into separate files.

#### Options

- `<pdf_file>`: The PDF file from which you want to extract pages.

## Examples

1.  Extract content from all PDFs in the current directory (output to `./pdfcor_output`):
    ```
    pdfcor process
    ```
    (If `--input-folder` is not specified, it defaults to the current directory. If `--output-folder` is not specified, it defaults to `pdfcor_output` inside the input directory.)

2.  Merge all PDFs in a folder, specifying the name and location of the merged file:
    ```
    pdfcor merge --input-folder /path/to/pdfs --output-file /path/to/other_folder/merged.pdf
    ```
    To save in the input folder with a specific name:
    ```
    pdfcor merge --input-folder /path/to/pdfs --output-file local_merge.pdf
    ```

3.  Extract pages from a specific PDF:
    ```
    pdfcor extract example.pdf
    ```

## Using as a Python Module

You can also use pdfcor as a module in your Python scripts:

```python
from pdfcor import process_pdf, process_folder, merge_pdfs, extract_pages

# Process a single PDF file
process_pdf("/path/to/file.pdf", "/path/to/output", resize=False)

# Process an entire folder
process_folder("/path/to/folder", "/path/to/output", recursive=True, resize=True)

# Merge PDFs
merge_pdfs("/path/to/folder", "merged_file.pdf") # Saves merged_file.pdf in /path/to/folder

# Extract pages from a PDF
extract_pages("/path/to/file.pdf")
```

## Features

- Extraction of textual content from PDFs into Markdown format
- Extraction and saving of images contained in PDFs
- Optional recursive processing of subfolders
- Optional resizing of images for A4 layout
- Merging of multiple PDF files into a single document
- Extraction of individual pages from a PDF
- Usable from the command line or as a Python module
- Informational and error messages via the `logging` module

## How It Works

pdfcor offers several main functionalities:

1.  **Markdown Content Extraction**:
    - Opens the PDF file using PyMuPDF (fitz)
    - Extracts text and images page by page
    - Converts the extracted text to Markdown format
    - Saves the extracted images and inserts references into the Markdown

2.  **PDF Merging**:
    - Reads all PDF files in the specified folder
    - Combines all PDFs into a single document
    - Saves the merged document (default name based on folder if `--output-file` is not used)

3.  **Page Extraction**:
    - Opens the specified PDF file
    - Creates a new PDF for each page
    - Saves the individual pages in a dedicated folder (named `pages-<slugified_pdf_name>`) in the same directory as the original PDF.

## Logging

pdfcor uses Python's `logging` module to display informational and error messages. When used as a library, the logging behavior can be customized like any standard Python application using this module.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request on our GitHub repository.

### Development Setup

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

### Code Style and Quality

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

### Running Tests

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

This project is licensed under the MIT License. See the `LICENSE` file for more details.