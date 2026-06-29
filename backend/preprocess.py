"""Text and structured-feature preprocessing used during inference."""

from __future__ import annotations

import re

import numpy as np

WEIGHT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s?(?:kg|g|ml|l)\b")
PACK_PATTERN = re.compile(r"\bpack of (\d+)\b")


def normalize_description(description: str) -> str:
    """Match the lowercase, whitespace-normalized notebook preprocessing."""
    return re.sub(r"\s+", " ", description).strip().lower()


def extract_structured_features(description: str) -> np.ndarray:
    """Extract the weight and pack-size values used by the trained model."""
    normalized = normalize_description(description)
    weight_match = WEIGHT_PATTERN.search(normalized)
    pack_match = PACK_PATTERN.search(normalized)
    weight = float(weight_match.group(1)) if weight_match else 0.0
    pack_size = int(pack_match.group(1)) if pack_match else 1
    return np.asarray([[weight, pack_size]], dtype=np.float32)
