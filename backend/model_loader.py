"""Lazy-loading utilities for the trained PriceVision inference stack."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "data" / "optimized_model.pkl"
TRAINING_DATA_PATH = PROJECT_ROOT / "data" / "sample_5000.csv"
EXPECTED_TEXT_FEATURES = 50_000


class ModelAssetError(RuntimeError):
    """Raised when a required inference artifact cannot be loaded."""


@lru_cache(maxsize=1)
def load_regressor() -> Any:
    """Load and cache the pre-trained XGBoost model."""
    if not MODEL_PATH.exists():
        raise ModelAssetError(
            f"Trained model not found at {MODEL_PATH}. "
            "Place optimized_model.pkl in the data directory."
        )
    try:
        return joblib.load(MODEL_PATH)
    except Exception as exc:
        raise ModelAssetError(f"Unable to load the trained model: {exc}") from exc


@lru_cache(maxsize=1)
def load_vectorizer() -> TfidfVectorizer:
    """Rebuild the notebook's deterministic TF-IDF vocabulary and cache it.

    The training notebook saved the regressor but not its fitted vectorizer.
    Fitting on the original, ordered training corpus recreates the exact
    vocabulary used by the model without retraining the price regressor.
    """
    if not TRAINING_DATA_PATH.exists():
        raise ModelAssetError(
            f"Vectorizer source data not found at {TRAINING_DATA_PATH}."
        )

    frame = pd.read_csv(TRAINING_DATA_PATH, usecols=["catalog_content"])
    corpus = (
        frame["catalog_content"]
        .astype(str)
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    vectorizer = TfidfVectorizer(
        max_features=EXPECTED_TEXT_FEATURES,
        ngram_range=(1, 3),
        min_df=2,
        stop_words="english",
    )
    vectorizer.fit(corpus)

    if len(vectorizer.vocabulary_) != EXPECTED_TEXT_FEATURES:
        raise ModelAssetError(
            "The reconstructed text vocabulary does not match the trained "
            f"model ({len(vectorizer.vocabulary_):,} features found)."
        )
    return vectorizer


@lru_cache(maxsize=1)
def load_image_encoder() -> Any:
    """Load and cache EfficientNetB0 as a 1,280-dimensional encoder."""
    try:
        from tensorflow.keras import backend as keras_backend
        from tensorflow.keras.applications import EfficientNetB0
        from tensorflow.keras.utils import get_file

        keras_backend.set_image_data_format("channels_last")
        encoder = EfficientNetB0(
            weights=None,
            include_top=False,
            input_shape=(224, 224, 3),
            pooling="avg",
        )
        weights_path = get_file(
            "efficientnetb0_notop.h5",
            "https://storage.googleapis.com/keras-applications/"
            "efficientnetb0_notop.h5",
            cache_subdir="models",
            file_hash="50bc09e76180e00e4465e1a485ddc09d",
        )
        encoder.load_weights(weights_path)
        return encoder
    except Exception as exc:
        raise ModelAssetError(
            "EfficientNetB0 could not be initialized. Ensure TensorFlow is "
            "installed and its ImageNet weights are available."
        ) from exc
