import io
import logging
from pathlib import Path
from typing import Any, List, Optional  # Any for fitz text blocks for now

import fitz  # PyMuPDF
from PIL import Image
from PIL.Image import Image as PillowImage  # For type hinting

from .utils import resize_for_a4, slugify


def _ensure_dir_exists(directory_path: Path) -> None:
    """Ensures that a directory exists, creating it if necessary."""
    directory_path.mkdir(parents=True, exist_ok=True)


def process_pdf(pdf_path: Path, output_dir: Path, resize: bool = False) -> None:
    """
    Processes a single PDF file, extracts text and images, and saves them as a Markdown file.

    Args:
        pdf_path (Path): The path to the PDF file.
        output_dir (Path): The directory where the Markdown file and images will be saved.
        resize (bool, optional): Whether to resize images to fit A4 paper. Defaults to False.
    """
    file_name_stem: str = pdf_path.stem
    file_name_slug: str = slugify(
        file_name_stem
    )  # Slugified name for image folder and image files

    img_dir: Path = output_dir / f"img-{file_name_slug}"
    _ensure_dir_exists(img_dir)

    doc: fitz.Document = fitz.open(pdf_path)  # type: ignore

    markdown_content: str = f"# {file_name_stem}\n\n"
    image_count: int = 0

    for page_num in range(len(doc)):
        page: fitz.Page = doc[page_num]  # type: ignore

        # Type for block: fitz uses tuples, could be List[Tuple[float, float, float, float, str, int, int]]
        # For simplicity, using List[Any] or more specific Tuple if known
        blocks: List[Any] = page.get_text("blocks")  # type: ignore
        for block in blocks:
            if block[6] == 0:  # block[6] == 0 indicates a text block
                markdown_content += block[4] + "\n\n"  # block[4] is the text content

        image_list: List[Any] = page.get_images()  # type: ignore
        for img_info in image_list:
            xref: int = img_info[0]
            base_image: Optional[dict] = doc.extract_image(xref)  # type: ignore

            if base_image is None or "image" not in base_image:
                logging.warning(
                    f"Could not extract image with xref {xref} from {pdf_path.name}"
                )
                continue

            image_bytes: bytes = base_image["image"]

            try:
                image: PillowImage = Image.open(io.BytesIO(image_bytes))
                image_count += 1

                resized_image: PillowImage
                if resize:
                    resized_image = resize_for_a4(image)
                else:
                    resized_image = image

                ext: str = base_image["ext"]
                if ext == "jpeg":
                    ext = "jpg"

                image_filename: str = f"{file_name_slug}-{image_count:02d}.{ext}"
                image_path: Path = img_dir / image_filename
                resized_image.save(image_path)

                markdown_content += (
                    f"![Image {image_count}](img-{file_name_slug}/{image_filename})\n\n"
                )
            except Exception as e:
                logging.error(
                    f"Error processing image {image_count} in {pdf_path.name}: {str(e)}"
                )

        if page_num < len(doc) - 1:
            markdown_content += "---\n\n"

    md_file_path: Path = output_dir / f"{file_name_stem}.md"
    md_file_path.write_text(markdown_content, encoding="utf-8")
    logging.info(f"Markdown file created at {md_file_path}")


def process_folder(
    folder_path: Path, output_dir: Path, recursive: bool = False, resize: bool = False
) -> None:
    """
    Processes all PDF files in a given folder (and its subfolders if recursive is True).

    Args:
        folder_path (Path): The path to the folder containing PDF files.
        output_dir (Path): The directory where the processed files will be saved.
        recursive (bool, optional): Whether to process PDF files in subfolders. Defaults to False.
        resize (bool, optional): Whether to resize images to fit A4 paper. Defaults to False.
    """
    pattern: str = "*.pdf"
    pdf_files_generator = (
        folder_path.rglob(pattern) if recursive else folder_path.glob(pattern)
    )

    count: int = 0
    for pdf_file_path in pdf_files_generator:
        if pdf_file_path.is_file():
            logging.info(f"Processing PDF: {pdf_file_path.name}...")
            process_pdf(pdf_file_path, output_dir, resize=resize)
            count += 1
    if count == 0:
        logging.warning(
            f"No PDF files found in {folder_path} {'(recursively)' if recursive else ''}"
        )


def merge_pdfs(
    input_folder: Path,
    output_file: Optional[str] = None,
    output_dir: Optional[Path] = None,
) -> None:
    """
    Merges all PDFs in a folder into a single file.

    Args:
        input_folder (Path): Path to the folder containing PDFs to merge.
        output_file (Optional[str], optional): Name of the output file.
                                     Defaults to slugify(folder_name) + ".pdf".
        output_dir (Optional[Path], optional): Directory to save the merged PDF.
                                    Defaults to input_folder.
    """
    input_folder_abs: Path = input_folder.resolve()
    output_filename_str: str

    if output_file is None:
        folder_name_candidate: str = input_folder_abs.name
        if (
            not folder_name_candidate
        ):  # Should be rare with Path objects (e.g. root path '/')
            folder_name_candidate = Path.cwd().name
        if not folder_name_candidate:  # Even rarer, if CWD is somehow root and unnamed
            folder_name_candidate = "merged-document"
        output_filename_str = slugify(folder_name_candidate) + ".pdf"
    else:
        output_filename_str = output_file

    effective_output_dir: Path = (
        output_dir.resolve() if output_dir else input_folder_abs
    )
    _ensure_dir_exists(effective_output_dir)

    pdf_files: List[Path] = sorted(
        [
            f
            for f in input_folder_abs.iterdir()
            if f.is_file() and f.suffix.lower() == ".pdf"
        ]
    )

    if not pdf_files:
        logging.warning(f"No PDF files found in folder {input_folder_abs}")
        return

    merged_pdf: fitz.Document = fitz.open()  # type: ignore
    for pdf_path in pdf_files:
        try:
            with fitz.open(pdf_path) as pdf_doc:  # type: ignore
                merged_pdf.insert_pdf(pdf_doc)  # type: ignore
        except Exception as e:
            logging.error(f"Error processing or inserting {pdf_path.name}: {e}")
            continue  # Skip problematic PDF

    output_path: Path = effective_output_dir / output_filename_str
    try:
        merged_pdf.save(
            str(output_path)
        )  # fitz typically wants str path, though some versions may take Path
    except Exception as e:
        logging.error(f"Failed to save merged PDF {output_path}: {e}")
    finally:
        merged_pdf.close()

    if (
        Path(output_path).exists() and Path(output_path).stat().st_size > 0
    ):  # Check if file was actually created and non-empty
        logging.info(f"PDFs merged into {output_path}")
    else:
        logging.error(
            f"Failed to create or save merged PDF: {output_path}. It might be empty or not created."
        )


def extract_pages(pdf_path: Path) -> None:
    """
    Extracts all pages from a PDF into separate files.

    Args:
        pdf_path (Path): Path to the PDF file to process.
    """
    pdf_name_slug: str = slugify(pdf_path.stem)
    output_folder_name: str = f"pages-{pdf_name_slug}"
    output_folder: Path = pdf_path.parent / output_folder_name
    _ensure_dir_exists(output_folder)

    try:
        with fitz.open(pdf_path) as pdf:  # type: ignore
            if pdf.page_count == 0:
                logging.warning(f"No pages found in PDF: {pdf_path.name}")
                return

            for page_num in range(pdf.page_count):
                output_pdf: fitz.Document = fitz.open()  # type: ignore
                try:
                    output_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)  # type: ignore
                    output_filename: str = f"{pdf_name_slug}-{page_num + 1:02d}.pdf"
                    output_file_path: Path = output_folder / output_filename
                    output_pdf.save(
                        str(output_file_path)
                    )  # fitz typically wants str path
                except Exception as e:
                    logging.error(
                        f"Error extracting page {page_num+1} from {pdf_path.name}: {e}"
                    )
                finally:
                    output_pdf.close()
        logging.info(f"Pages extracted to folder {output_folder}")
    except Exception as e:
        logging.error(
            f"Failed to open or process PDF {pdf_path.name} for page extraction: {e}"
        )
