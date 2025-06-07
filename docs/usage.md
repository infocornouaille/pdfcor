# Usage Guide

## Command-Line Interface (CLI)

pdfcor can be used from the command line with various options, structured into commands.

### Processing PDFs to Markdown

Command: `pdfcor process [OPTIONS]`

(Example: `pdfcor process --input-folder <input_folder> --output-folder <output_folder> [--recursive] [--resize]`)

**Options**:

- `--input-folder`: Specifies the input folder containing the PDF files to process. By default, it uses the current directory.
- `--output-folder`: Defines the output folder for the Markdown files and extracted images. If not specified, it uses a subfolder named `pdfcor_output` within the input folder.
- `--recursive` / `-r`: Enables recursive processing of subfolders.
- `--resize`: Resizes extracted images to fit on an A4 page.

### Merging PDFs

Command: `pdfcor merge [OPTIONS]`

(Example: `pdfcor merge --input-folder <input_folder> --output-file <output_filename_or_path>`)

This command merges all PDFs in a folder without any transformation.

**Options**:

- `--input-folder`: Specifies the folder containing the PDFs to merge. By default, uses the current directory.
- `--output-file`: Specifies the name and/or path of the merged PDF file.
    - If only a name is provided (e.g., `my_file.pdf`), the merged PDF will be saved in the input folder (`--input-folder`).
    - If a full path is provided (e.g., `/another/folder/my_file.pdf`), it will be saved to that location.
    - If this option is not used, the merged file will be named after the input folder (e.g., `input_folder_name.pdf`) and saved in that same input folder.

### Extracting Pages

Command: `pdfcor extract <pdf_file>`

This command extracts all pages from a PDF into separate files.

**Arguments**:

- `<pdf_file>`: The PDF file from which you want to extract pages. (Required)

## CLI Examples

1.  **Extract content from all PDFs in the current directory** (output to `./pdfcor_output`):
    ```bash
    pdfcor process
    ```
    (If `--input-folder` is not specified, it defaults to the current directory. If `--output-folder` is not specified, it defaults to `pdfcor_output` inside the input directory.)

2.  **Merge all PDFs in a folder**, specifying the name and location of the merged file:
    ```bash
    pdfcor merge --input-folder /path/to/pdfs --output-file /path/to/other_folder/merged.pdf
    ```
    To save in the input folder with a specific name:
    ```bash
    pdfcor merge --input-folder /path/to/pdfs --output-file local_merge.pdf
    ```

3.  **Extract pages from a specific PDF**:
    ```bash
    pdfcor extract example.pdf
    ```

## Using as a Python Module

You can also use pdfcor as a module in your Python scripts:

```python
from pdfcor import process_pdf, process_folder, merge_pdfs, extract_pages
from pathlib import Path # Import Path for Path objects
from typing import Optional # For Optional type hints

# Process a single PDF file
# process_pdf(pdf_path: Path, output_dir: Path, resize: bool = False)
process_pdf(Path("/path/to/file.pdf"), Path("/path/to/output"), resize=False)

# Process an entire folder
# process_folder(folder_path: Path, output_dir: Path, recursive: bool = False, resize: bool = False)
process_folder(Path("/path/to/folder"), Path("/path/to/output"), recursive=True, resize=True)

# Merge PDFs
# merge_pdfs(input_folder: Path, output_file: Optional[str] = None, output_dir: Optional[Path] = None)
merge_pdfs(Path("/path/to/folder"), output_file="merged_file.pdf") # Saves merged_file.pdf in /path/to/folder

# Extract pages from a PDF
# extract_pages(pdf_path: Path)
extract_pages(Path("/path/to/file.pdf"))
```
Note: The core functions now expect `pathlib.Path` objects for path arguments.
