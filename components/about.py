"""About, architecture, and technology sections."""

from __future__ import annotations

import streamlit as st

from components.navbar import GITHUB_URL


def render_about() -> None:
    """Explain the product and its preserved model architecture."""
    st.markdown('<div id="about"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-heading">
          <span>Inside PriceVision AI</span>
          <h2>Production architecture for multimodal pricing.</h2>
          <p>
            A complete inference path from raw product inputs to a report-ready
            price estimate, without retraining or simplifying the model.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tech_cards = (
        ("TXT", "TF-IDF", "50,000 language features", "Product description"),
        ("IMG", "EfficientNetB0", "1,280 visual features", "Product image"),
        ("SUM", "Feature Fusion", "51,282 total features", "Unified signal"),
        ("XGB", "XGBoost", "Optimized regressor", "USD prediction"),
    )
    columns = st.columns(4, gap="small")
    for column, (icon, title, value, caption) in zip(columns, tech_cards):
        with column:
            st.markdown(
                f"""
                <article class="tech-card">
                  <div class="tech-icon">{icon}</div>
                  <span>{caption}</span><h3>{title}</h3><p>{value}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div id="model"></div>', unsafe_allow_html=True)
    flow_col, copy_col = st.columns([0.6, 0.4], gap="large")
    with flow_col:
        st.markdown(
            """
            <section class="architecture-card" id="architecture">
              <div class="architecture-title">
                <span>Model Architecture</span><b>Live pipeline</b>
              </div>
              <div class="flow-nodes">
                <div><i>01</i><b>Text</b><span>Product description</span></div>
                <em>-></em>
                <div><i>02</i><b>TF-IDF</b><span>Language vectors</span></div>
                <em>-></em>
                <div><i>03</i><b>EfficientNetB0</b><span>Image embeddings</span></div>
                <em>-></em>
                <div><i>04</i><b>Feature Fusion</b><span>51,282 features</span></div>
                <em>-></em>
                <div class="flow-final"><i>05</i><b>XGBoost</b><span>Prediction</span></div>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with copy_col:
        st.markdown(
            f"""
            <section class="about-copy-card">
              <span>Why multimodal?</span>
              <h3>Products communicate value through more than text.</h3>
              <p>
                Language captures specifications. Images reveal appearance.
                Package attributes add commercial context. PriceVision AI
                brings those signals together in one focused workflow.
              </p>
              <a href="{GITHUB_URL}" target="_blank" rel="noopener">
                Explore the project
              </a>
            </section>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    """Render the product footer."""
    st.markdown(
        f"""
        <footer class="site-footer">
          <div class="footer-brand">
            <div><span class="footer-logo">PV</span><strong>PriceVision AI</strong></div>
            <p>Multimodal price intelligence for modern commerce.</p>
            <small>Built with care using the preserved ML pipeline.</small>
          </div>
          <div class="footer-column"><b>Product</b>
            <a href="#predict">Predict Price</a><a href="#architecture">How It Works</a>
            <a href="#about">About</a><a href="#model">Model Details</a>
          </div>
          <div class="footer-column"><b>Technology</b>
            <span>TensorFlow</span><span>EfficientNetB0</span>
            <span>TF-IDF</span><span>XGBoost</span><span>Streamlit</span>
          </div>
          <div class="footer-column"><b>Resources</b>
            <a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub</a>
            <span>Documentation</span><span>Dataset</span><span>PDF Reports</span>
          </div>
        </footer>
        <div class="footer-bottom">
          <span>&copy; 2026 PriceVision AI. All rights reserved.</span>
          <span>Privacy Policy</span>
          <span>Terms of Use</span>
          <span>Disclaimer</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
