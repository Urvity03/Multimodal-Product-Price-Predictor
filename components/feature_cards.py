"""Product capability strip."""

from __future__ import annotations

import streamlit as st

FEATURES = (
    (
        "bolt",
        "Fast Predictions",
        "Cached inference pipeline delivers results in seconds.",
    ),
    (
        "brain",
        "Multimodal AI",
        "Text, image, and structured features work together.",
    ),
    (
        "target",
        "Optimized Model",
        "XGBoost powered by EfficientNetB0 and TF-IDF.",
    ),
    (
        "shield",
        "Reliable & Accurate",
        "Validated inputs with honest model reporting.",
    ),
)


def render_features() -> None:
    """Render the premium horizontal feature strip."""
    columns = st.columns(4, gap="large")
    for column, (icon, title, body) in zip(columns, FEATURES):
        with column:
            st.markdown(f"#### {title}")
            st.write(body)
