# Installation

## Standard Installation

```bash
pip install pdfcor
```

### Using pipx (Recommended for CLI tool)

If you want to use `pdfcor` as a command-line tool, `pipx` is recommended as it installs the package in an isolated environment and makes its entry points available system-wide.

First, ensure `pipx` is installed:
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

Then, install `pdfcor` using `pipx`:
```bash
pipx install pdfcor
```
Now you can run `pdfcor` commands directly from your terminal. To upgrade later: `pipx upgrade pdfcor`.

### Using uv (Alternative Installer)

If you prefer using `uv` (a fast Python package installer), you can install `pdfcor` with:
```bash
uv pip install pdfcor
```
This is an alternative to using `pip`.

## Dependencies

pdfcor depends on the following libraries:

- PyMuPDF (fitz): for extracting content from PDFs and manipulating PDF files
- Pillow (PIL): for image processing

These dependencies will be automatically installed when you install pdfcor via pip (or the chosen installer).
