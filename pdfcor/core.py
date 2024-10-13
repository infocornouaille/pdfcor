import os
import fitz
from PIL import Image
import io
from .utils import slugify, resize_for_a4


def process_pdf(pdf_path, output_dir, rezise=False):
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    img_dir = os.path.join(output_dir, f"img-{slugify(file_name)}")
    os.makedirs(img_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    markdown_content = f"# {file_name}\n\n"
    image_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        blocks = page.get_text("blocks")
        for block in blocks:
            if block[6] == 0:  # Type texte
                markdown_content += block[4] + "\n\n"

        image_list = page.get_images()
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            try:
                image = Image.open(io.BytesIO(image_bytes))
                image_count += 1
                if rezise:
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
                print(
                    f"Erreur lors du traitement de l'image {image_count} dans {file_name}: {str(e)}"
                )

        if page_num < len(doc) - 1:
            markdown_content += "---\n\n"

    with open(os.path.join(output_dir, f"{file_name}.md"), "w", encoding="utf-8") as f:
        f.write(markdown_content)


def process_folder(folder_path, output_dir, recursive=False, resize=False):
    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    process_pdf(pdf_path, output_dir, resize)
    else:
        for file in os.listdir(folder_path):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(folder_path, file)
                process_pdf(pdf_path, output_dir, resize)


def merge_pdfs(input_folder, output_file=None):
    """
    Fusionne tous les PDF d'un dossier en un seul fichier.

    :param input_folder: Chemin du dossier contenant les PDF à fusionner
    :param output_file: Nom du fichier de sortie (optionnel)
    """
    input_folder = os.path.abspath(input_folder)

    if output_file is None:
        folder_name = os.path.basename(input_folder)
        if folder_name == "":  # Cas où input_folder est "."
            folder_name = os.path.basename(os.getcwd())
        output_file = folder_name + ".pdf"

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    pdf_files.sort()  # Trie les fichiers par ordre alphabétique

    if not pdf_files:
        print(f"Aucun fichier PDF trouvé dans le dossier {input_folder}")
        return

    merged_pdf = fitz.open()

    for pdf_file in pdf_files:
        with fitz.open(os.path.join(input_folder, pdf_file)) as pdf:
            merged_pdf.insert_pdf(pdf)

    output_path = os.path.join(input_folder, output_file)
    merged_pdf.save(output_path)
    merged_pdf.close()

    print(f"Les PDF ont été fusionnés dans {output_path}")


def extract_pages(pdf_path):
    """
    Extrait toutes les pages d'un PDF dans des fichiers séparés.

    :param pdf_path: Chemin du fichier PDF à traiter
    """
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_name = slugify(pdf_name)
    output_folder = f"pages-{pdf_name}"
    os.makedirs(output_folder, exist_ok=True)

    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            output_pdf = fitz.open()
            output_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)
            output_file = os.path.join(
                output_folder, f"{pdf_name}-{page_num+1:02d}.pdf"
            )
            output_pdf.save(output_file)
            output_pdf.close()

    print(f"Les pages ont été extraites dans le dossier {output_folder}")
