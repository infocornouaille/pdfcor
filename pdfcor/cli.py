from pathlib import Path
from typing import Optional

import typer

# Assuming core functions are in .core relative to this cli.py file
from .core import extract_pages, merge_pdfs, process_folder
from .utils import slugify  # Import slugify

app = typer.Typer(
    name="pdfcor",
    help="pdfcor: A versatile Python package for PDF manipulation.",
    add_completion=False,  # Disable shell completion for simplicity in this context
    no_args_is_help=True,  # Show help if no command is given
)


@app.command(
    "process", help="Extracts content from PDFs to Markdown, including images."
)
def process_cli(
    input_folder: Path = typer.Option(
        Path("."),
        "--input-folder",
        "-i",
        help="Input folder containing PDF files to process.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        show_default="current directory",
    ),
    output_folder_opt: Optional[Path] = typer.Option(
        None,
        "--output-folder",
        "-o",
        help="Output folder for Markdown files and extracted images. Defaults to 'pdfcor_output' inside the input folder.",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,  # resolve_path for user convenience
        show_default="None (uses 'pdfcor_output' in input folder)",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively process subfolders within the input folder.",
    ),
    resize: bool = typer.Option(
        False, "--resize", help="Resize extracted images to fit A4 page dimensions."
    ),
) -> None:
    """
    Processes PDF files in INPUT_FOLDER, extracts text and images to Markdown.
    """
    actual_output_folder: Path
    if output_folder_opt is None:
        actual_output_folder = input_folder / "pdfcor_output"
    else:
        actual_output_folder = output_folder_opt

    # core.process_pdf (called by process_folder) handles img_dir creation
    # core.process_pdf writes .md file to actual_output_folder, so it must exist
    actual_output_folder.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Processing PDFs from: {input_folder}")
    typer.echo(f"Outputting Markdown and images to: {actual_output_folder}")
    process_folder(input_folder, actual_output_folder, recursive, resize)
    typer.echo("PDF processing complete.")


@app.command("merge", help="Merges all PDF files in a specified input folder.")
def merge_cli(
    input_folder: Path = typer.Option(
        Path("."),
        "--input-folder",
        "-i",
        help="Input folder containing PDF files to merge.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        show_default="current directory",
    ),
    output_file_opt: Optional[
        Path
    ] = typer.Option(  # Changed from output_path_opt to output_file_opt for clarity
        None,
        "--output-file",
        "-out",
        help="Path for the merged PDF (e.g., merged.pdf or /path/to/merged.pdf). Default: auto-named in input folder.",
        # resolve_path=True means Typer resolves it. If user gives filename, it's resolved in CWD.
        # If user gives ../filename, it's resolved relative to CWD.
        # This behavior is fine as core.merge_pdfs can handle it.
        writable=True,
        dir_okay=False,
        resolve_path=True,  # Allow creating the file
        show_default="None (auto-named in input folder)",
    ),
) -> None:
    """
    Merges all PDF files found in INPUT_FOLDER.
    The output file can be specified using --output-file.
    """
    output_filename_arg: Optional[str] = None
    output_dir_arg: Optional[Path] = None

    if output_file_opt:
        # If output_file_opt.parent is '.', it means it's a filename in the CWD (if not absolute)
        # or just a filename if it was passed as 'name.pdf'
        # Path.resolve() on 'name.pdf' makes it '/cwd/path/name.pdf'
        # Path('some/dir/name.pdf').resolve() makes it '/cwd/path/some/dir/name.pdf'

        # If the resolved path's parent directory is the current working directory,
        # AND the original option string didn't specify a directory,
        # then it's likely just a filename, and we want it in the input_folder.
        # However, Typer with resolve_path=True already makes it absolute.
        # The core.merge_pdfs function is smart:
        # - if output_dir is None, it uses input_folder.
        # - if output_file is None, it generates a name.

        # If user provides "merged.pdf", output_file_opt.name = "merged.pdf", output_file_opt.parent = Path('.') (after resolve, CWD)
        # If user provides "output/merged.pdf", output_file_opt.name = "merged.pdf", output_file_opt.parent = Path('output') (after resolve, CWD/output)

        # Simplified logic: core.merge_pdfs will handle defaults if args are None.
        # If output_file_opt is provided, we use its name and its parent as the directory.
        output_dir_arg = output_file_opt.parent
        output_filename_arg = output_file_opt.name

    # If output_file_opt is None, both output_filename_arg and output_dir_arg remain None.
    # core.merge_pdfs will then use input_folder as output_dir and generate a default filename.

    typer.echo(f"Merging PDFs from: {input_folder}")
    # Inform user about actual output location based on core.merge_pdfs logic
    final_output_dir = output_dir_arg if output_dir_arg is not None else input_folder
    final_output_name = (
        output_filename_arg
        if output_filename_arg is not None
        else f"{slugify(input_folder.name)}.pdf"
    )  # Replicate core's default name for echo

    if output_file_opt:
        typer.echo(f"Saving merged PDF as: {final_output_dir / final_output_name}")
    else:
        typer.echo(f"Saving merged PDF with default name in: {final_output_dir}")

    merge_pdfs(input_folder, output_file=output_filename_arg, output_dir=output_dir_arg)
    # Successful output message is handled by merge_pdfs logging


@app.command("extract", help="Extracts all pages from a PDF into separate files.")
def extract_cli(
    pdf_file: Path = typer.Argument(
        ...,  # Ellipsis makes it a required argument
        help="The PDF file to extract pages from.",
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        resolve_path=True,
        show_default=False,  # Not useful for Arguments
    ),
) -> None:
    """
    Extracts all pages from PDF_FILE into a 'pages-<pdf_name>' subfolder
    created in the same directory as the PDF_FILE.
    """
    typer.echo(f"Extracting pages from: {pdf_file}")
    extract_pages(pdf_file)
    # Successful output message is handled by extract_pages logging


if __name__ == "__main__":
    app()
