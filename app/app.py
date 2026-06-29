"""PriceVision AI Streamlit application entry point."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.about import render_about, render_footer
from components.feature_cards import render_features
from components.hero import render_hero
from components.navbar import render_navbar
from components.prediction_form import render_prediction_form
from components.results import render_results

st.set_page_config(
    page_title="PriceVision AI - Multimodal Price Intelligence",
    page_icon="PV",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": (
            "PriceVision AI combines product text, imagery, and structured "
            "features to generate a model-based price estimate."
        )
    },
)


def load_styles() -> None:
    """Inject the single project design-system stylesheet."""
    css_path = PROJECT_ROOT / "styles" / "styles.css"
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def main() -> None:
    """Compose the complete single-page application."""
    load_styles()
    render_navbar()
    render_hero()
    render_features()
    render_prediction_form()
    render_results()
    render_about()
    render_footer()


if __name__ == "__main__":
    main()
