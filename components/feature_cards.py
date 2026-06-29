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
    items = "".join(
        f"""
        <article class="feature-item">
          <div class="feature-icon {icon}" aria-hidden="true"></div>
          <div><h3>{title}</h3><p>{body}</p></div>
        </article>
        """
        for icon, title, body in FEATURES
    )
    st.markdown(
        f'<section class="feature-strip" aria-label="Core capabilities">{items}</section>',
        unsafe_allow_html=True,
    )
