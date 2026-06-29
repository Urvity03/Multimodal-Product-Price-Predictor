"""Image validation and EfficientNetB0 feature extraction."""

from __future__ import annotations

from io import BytesIO

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from backend.model_loader import load_image_encoder

MAX_IMAGE_BYTES = 10 * 1024 * 1024
IMAGE_SIZE = (224, 224)


class ImageValidationError(ValueError):
    """Raised when an uploaded file is not a usable product image."""


def open_product_image(image_bytes: bytes) -> Image.Image:
    """Validate bytes and return a correctly oriented RGB image."""
    if not image_bytes:
        raise ImageValidationError("Please upload a product image.")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise ImageValidationError("The image must be smaller than 10 MB.")
    try:
        image = Image.open(BytesIO(image_bytes))
        image.verify()
        image = Image.open(BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise ImageValidationError(
            "The uploaded file is not a valid JPG, PNG, or WebP image."
        ) from exc
    if image.width < 32 or image.height < 32:
        raise ImageValidationError("The image is too small to analyze.")
    return image


def extract_image_features(image_bytes: bytes) -> np.ndarray:
    """Create the 1,280 visual features expected by the regressor."""
    image = open_product_image(image_bytes)
    image = ImageOps.fit(image, IMAGE_SIZE, method=Image.Resampling.LANCZOS)
    batch = np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)

    # EfficientNet in modern Keras contains input rescaling internally.
    features = load_image_encoder().predict(batch, verbose=0)
    return np.asarray(features, dtype=np.float32)
