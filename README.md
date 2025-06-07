# pdfcor

![PyPI version](https://img.shields.io/pypi/v/pdfcor.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pdfcor.svg)

pdfcor is a versatile Python package for working with PDF files. It allows you to extract content in Markdown format with images, merge PDFs, and extract individual pages.

## Installation

```
pip install pdfcor
```

## Dependencies

pdfcor depends on the following libraries:

- PyMuPDF (fitz): for extracting content from PDFs and manipulating PDF files
- Pillow (PIL): for image processing

These dependencies will be automatically installed when you install pdfcor via pip.

## Usage

pdfcor can be used from the command line with various options:

### Extracting Content to Markdown

```
pdfcor --input-folder <input_folder> --output-folder <output_folder> [--recursive] [--resize]
```

#### Options

- `--input-folder`: Specifies the input folder containing the PDF files to process. By default, it uses the current directory.
- `--output-folder`: Defines the output folder for the Markdown files and extracted images. If not specified, it uses a subfolder named `pdfcor_output` within the input folder.
- `--recursive`: Enables recursive processing of subfolders.
- `--resize`: Resizes extracted images to fit on an A4 page.

### Merging PDFs

```
pdfcor --fusion [--input-folder <input_folder>] [--output-file <output_filename_or_path>]
```

This command merges all PDFs in a folder without any transformation.

#### Options

- `--input-folder`: Specifies the folder containing the PDFs to merge. By default, uses the current directory.
- `--output-file`: Specifies the name and/or path of the merged PDF file.
    - If only a name is provided (e.g., `my_file.pdf`), the merged PDF will be saved in the input folder (`--input-folder`).
    - If a full path is provided (e.g., `/another/folder/my_file.pdf`), it will be saved to that location.
    - If this option is not used, the merged file will be named after the input folder (e.g., `input_folder_name.pdf`) and saved in that same input folder.

### Extracting Pages

```
pdfcor --pages <pdf_file>
```

This command extracts all pages from a PDF into separate files.

#### Options

- `<pdf_file>`: The PDF file from which you want to extract pages.

## Examples

1.  Extract content from all PDFs in the current directory (output to `./pdfcor_output`):
    ```
    pdfcor
    ```

2.  Merge all PDFs in a folder, specifying the name and location of the merged file:
    ```
    pdfcor --fusion --input-folder /path/to/pdfs --output-file /path/to/other_folder/merged.pdf
    ```
    To save in the input folder with a specific name:
    ```
    pdfcor --fusion --input-folder /path/to/pdfs --output-file local_merge.pdf
    ```

3.  Extract pages from a specific PDF:
    ```
    pdfcor --pages example.pdf
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

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.