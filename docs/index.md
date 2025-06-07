# Welcome to pdfcor

![PyPI version](https://img.shields.io/pypi/v/pdfcor.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pdfcor.svg)

pdfcor is a versatile Python package for working with PDF files. It allows you to extract content in Markdown format with images, merge PDFs, and extract individual pages.

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
