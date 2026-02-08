from PIL import Image
import io

MAX_IMAGE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def validate_image(file_content: bytes, filename: str) -> None:
    """
    Validates the image file size and extension.
    Raises ValueError if invalid.
    """
    # Check size
    if len(file_content) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"Image size exceeds {MAX_IMAGE_SIZE_MB}MB limit.")

    # Check extension
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    # Check if it's a valid image file
    try:
        img = Image.open(io.BytesIO(file_content))
        img.verify()
    except Exception:
        raise ValueError("Invalid image file content.")

def process_image(file_content: bytes) -> Image.Image:
    """
    Opens and converts image to RGB for processing.
    """
    image = Image.open(io.BytesIO(file_content))
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image
