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
