import re
from PIL import Image


def slugify(text):
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def resize_for_a4(image):
    a4_width, a4_height = 210, 297  # mm
    dpi = 300  # points per inch
    max_width = int(a4_width / 25.4 * dpi)
    max_height = int(a4_height / 25.4 * dpi)

    ratio = min(max_width / image.width, max_height / image.height)
    new_size = (int(image.width * ratio), int(image.height * ratio))
    return image.resize(new_size, Image.LANCZOS)
