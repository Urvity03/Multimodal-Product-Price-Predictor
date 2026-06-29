"""End-to-end product price prediction service."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.sparse import csr_matrix, hstack

from backend.image_utils import extract_image_features
from backend.model_loader import load_regressor, load_vectorizer
from backend.preprocess import (
    extract_structured_features,
    normalize_description,
)

MODEL_NAME = "Optimized XGBoost + EfficientNetB0"
USD_TO_INR = 86.20
MIN_DESCRIPTION_LENGTH = 20


@dataclass(frozen=True)
class PredictionResult:
    """Serializable values shown in the results dashboard."""

    usd: float
    inr: float
    elapsed_seconds: float
    model_name: str
    summary: str


def validate_description(description: str) -> str:
    """Validate and normalize user-entered product text."""
    normalized = normalize_description(description)
    if len(normalized) < MIN_DESCRIPTION_LENGTH:
        raise ValueError(
            "Add a more complete product description (at least 20 characters)."
        )
    if len(normalized) > 5_000:
        raise ValueError("Keep the product description under 5,000 characters.")
    return normalized


def predict_price(description: str, image_bytes: bytes) -> PredictionResult:
    """Run the preserved multimodal model and return display-ready values."""
    started = perf_counter()
    normalized = validate_description(description)

    text_features = load_vectorizer().transform([normalized])
    image_features = extract_image_features(image_bytes)
    structured_features = extract_structured_features(normalized)
    combined = hstack(
        [
            text_features,
            csr_matrix(image_features),
            csr_matrix(structured_features),
        ],
        format="csr",
    )

    regressor = load_regressor()
    expected = getattr(regressor, "n_features_in_", combined.shape[1])
    if combined.shape[1] != expected:
        raise RuntimeError(
            "Inference feature mismatch: "
            f"model expects {expected:,}, pipeline created "
            f"{combined.shape[1]:,}."
        )

    log_prediction = float(regressor.predict(combined)[0])
    usd = max(0.0, float(np.expm1(log_prediction)))
    elapsed = perf_counter() - started
    return PredictionResult(
        usd=usd,
        inr=usd * USD_TO_INR,
        elapsed_seconds=elapsed,
        model_name=MODEL_NAME,
        summary=(
            "This estimate combines language signals, visual product "
            "embeddings, and extracted package attributes."
        ),
    )
