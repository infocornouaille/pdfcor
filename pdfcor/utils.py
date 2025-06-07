import re

from PIL import Image  # Keep this for Image.LANCZOS and other Image module constants
from PIL.Image import Image as PillowImage  # For type hinting


def slugify(text: str) -> str:
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def resize_for_a4(image: PillowImage) -> PillowImage:
    a4_width: int = 210  # mm
    a4_height: int = 297  # mm
    dpi: int = 300  # points per inch
    # Convert mm to pixels: (mm / 25.4 inches/mm) * dpi
    max_width_px: int = int(a4_width / 25.4 * dpi)
    max_height_px: int = int(a4_height / 25.4 * dpi)

    if image.width == 0 or image.height == 0:  # Avoid division by zero for empty images
        # For a 0x0 image, resizing is tricky. Return a copy or a 1x1 placeholder?
        # Copying preserves it. If it needs to be valid for further Pillow ops, a 1x1 might be better.
        # However, the original code would have errored; copy is safer.
        return image.copy()

    ratio: float = min(max_width_px / image.width, max_height_px / image.height)

    new_width: int = int(image.width * ratio)
    new_height: int = int(image.height * ratio)

    # Ensure new dimensions are at least 1 pixel if original was not 0,
    # to avoid errors with image.resize((0,0), ...) or image.resize((x,0), ...)
    if new_width == 0 and image.width > 0:
        new_width = 1
    if new_height == 0 and image.height > 0:
        new_height = 1

    # If after adjustment, dimensions are still zero (e.g. original image was 0x0 and ratio made it 0)
    # This case is mostly covered by the initial check for image.width/height == 0.
    # But if ratio somehow resulted in 0 for a non-zero dimension image (e.g. extremely small float ratio * small int dim)
    if new_width == 0 or new_height == 0:
        return (
            image.copy()
        )  # Fallback to returning a copy if new dimensions are invalid

    new_size: tuple[int, int] = (new_width, new_height)
    return image.resize(new_size, Image.LANCZOS)
