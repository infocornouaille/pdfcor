import os
import fitz
from PIL import Image
import io
import logging
from .utils import slugify, resize_for_a4


def _ensure_dir_exists(directory_path):
    """Ensures that a directory exists, creating it if necessary."""
    os.makedirs(directory_path, exist_ok=True)


def process_pdf(pdf_path, output_dir, resize=False):
    """
    Processes a single PDF file, extracts text and images, and saves them as a Markdown file.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory where the Markdown file and images will be saved.
        resize (bool, optional): Whether to resize images to fit A4 paper. Defaults to False.
    """
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    img_dir = os.path.join(output_dir, f"img-{slugify(file_name)}")
    _ensure_dir_exists(img_dir)

    doc = fitz.open(pdf_path)

    markdown_content = f"# {file_name}\n\n"
    image_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        blocks = page.get_text("blocks")
        for block in blocks:
            if block[6] == 0:  # block[6] == 0 indicates a text block
                markdown_content += block[4] + "\n\n"

        image_list = page.get_images()
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            try:
                image = Image.open(io.BytesIO(image_bytes))
                image_count += 1
                if resize:
                    resized_image = resize_for_a4(image)
                else:
                    resized_image = image

                ext = base_image["ext"]
                if ext == "jpeg":
                    ext = "jpg"

                image_filename = f"{slugify(file_name)}-{image_count:02d}.{ext}"
                image_path = os.path.join(img_dir, image_filename)
                resized_image.save(image_path)

                markdown_content += f"![Image {image_count}](img-{slugify(file_name)}/{image_filename})\n\n"
            except Exception as e:
                logging.error(
                    f"Erreur lors du traitement de l'image {image_count} dans {file_name}: {str(e)}"
                )

        if page_num < len(doc) - 1:
            markdown_content += "---\n\n"

    with open(os.path.join(output_dir, f"{file_name}.md"), "w", encoding="utf-8") as f:
        f.write(markdown_content)


def process_folder(folder_path, output_dir, recursive=False, resize=False):
    """
    Processes all PDF files in a given folder (and its subfolders if recursive is True).

    Args:
        folder_path (str): The path to the folder containing PDF files.
        output_dir (str): The directory where the processed files will be saved.
        recursive (bool, optional): Whether to process PDF files in subfolders. Defaults to False.
        resize (bool, optional): Whether to resize images to fit A4 paper. Defaults to False.
    """
    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    process_pdf(pdf_path, output_dir, resize=resize)
    else:
        for file in os.listdir(folder_path):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, file)
                process_pdf(pdf_path, output_dir, resize=resize)


def merge_pdfs(input_folder, output_file=None, output_dir=None):
    """
    Merges all PDFs in a folder into a single file.

    Args:
        input_folder (str): Path to the folder containing PDFs to merge.
        output_file (str, optional): Name of the output file.
                                     Defaults to slugify(folder_name) + ".pdf".
        output_dir (str, optional): Directory to save the merged PDF.
                                    Defaults to input_folder.
    """
    input_folder_abs = os.path.abspath(input_folder)

    if output_file is None:
        # Try to get the folder name from the input_folder path itself
        folder_name_candidate = os.path.basename(input_folder_abs)
        if not folder_name_candidate:  # True if input_folder_abs was the root directory (e.g., '/')
            # Fallback to the name of the current working directory
            folder_name_candidate = os.path.basename(os.getcwd())
        # If somehow still empty (e.g. getcwd was root and basename was empty), use a generic default
        if not folder_name_candidate: # Should be very rare
            folder_name_candidate = "merged-document"
        output_filename = slugify(folder_name_candidate) + ".pdf"
    else:
        output_filename = output_file

    if output_dir is None:
        effective_output_dir = input_folder_abs
    else:
        effective_output_dir = os.path.abspath(output_dir)

    _ensure_dir_exists(effective_output_dir)

    pdf_files = [f for f in os.listdir(input_folder_abs) if f.lower().endswith(".pdf")]
    pdf_files.sort()

    if not pdf_files:
        logging.warning(f"Aucun fichier PDF trouvé dans le dossier {input_folder_abs}")
        return

    merged_pdf = fitz.open()

    for pdf_file_name in pdf_files:
        with fitz.open(os.path.join(input_folder_abs, pdf_file_name)) as pdf:
            merged_pdf.insert_pdf(pdf)

    output_path = os.path.join(effective_output_dir, output_filename)
    merged_pdf.save(output_path)
    merged_pdf.close()

    logging.info(f"Les PDF ont été fusionnés dans {output_path}")


def extract_pages(pdf_path):
    """
    Extrait toutes les pages d'un PDF dans des fichiers séparés.

    :param pdf_path: Chemin du fichier PDF à traiter
    """
    pdf_name_base = os.path.splitext(os.path.basename(pdf_path))[0]
    # pdf_name_base is the raw filename without extension, e.g., "My Document"
    # output_folder_name should be based on a slugified version, e.g., "pages-my-document"
    output_folder_name = f"pages-{slugify(pdf_name_base)}"
    output_folder = os.path.join(os.path.dirname(pdf_path), output_folder_name)
    _ensure_dir_exists(output_folder)

    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            output_pdf = fitz.open()
            output_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)
            output_filename = f"{slugify(pdf_name_base)}-{page_num+1:02d}.pdf"
            output_file_path = os.path.join(output_folder, output_filename)
            output_pdf.save(output_file_path)
            output_pdf.close()

    logging.info(f"Les pages ont été extraites dans le dossier {output_folder}")
