"""Sticky application navigation."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
GITHUB_URL = "https://github.com/Urvity03/Multimodal-Product-Price-Predictor"


def image_data_uri(path: Path) -> str:
    """Return a local PNG as an embeddable data URI."""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_navbar() -> None:
    """Render the floating glass navigation bar."""
    logo = image_data_uri(ASSETS_DIR / "logo.png")
    st.markdown(
        f"""
        <nav class="navbar" aria-label="Primary navigation">
          <a class="brand" href="#home" aria-label="PriceVision AI home">
            <span class="brand-mark"><img src="{logo}" alt=""></span>
            <span>PriceVision <strong>AI</strong></span>
          </a>
          <div class="nav-links">
            <a class="active" href="#home">Home</a>
            <a href="#predict">Predict</a>
            <a href="#about">About</a>
            <a href="#architecture">How It Works</a>
            <a href="#model">Model Details</a>
          </div>
          <a class="github-nav" href="{GITHUB_URL}" target="_blank"
             rel="noopener" aria-label="Open GitHub repository">
            <span class="github-icon" aria-hidden="true">GH</span>
            GitHub
            <span class="external-arrow" aria-hidden="true">/</span>
          </a>
        </nav>
        """,
        unsafe_allow_html=True,
    )
