"""Prediction results dashboard and report download."""

from __future__ import annotations

import html

import streamlit as st

from backend.predict import PredictionResult
from backend.utils import build_prediction_pdf


def _render_empty_results() -> None:
    """Render a non-placeholder empty state before the first prediction."""
    st.markdown(
        """
        <section class="results-empty" aria-label="Results preview">
          <div>
            <span>Results Dashboard</span>
            <h2>Model output appears here after a prediction.</h2>
            <p>
              PriceVision AI will show the USD estimate, approximate INR value,
              model runtime, analyzed image, prediction summary, and PDF export.
            </p>
          </div>
          <div class="empty-metrics" aria-hidden="true">
            <article><small>USD</small><b>Ready</b></article>
            <article><small>INR</small><b>Ready</b></article>
            <article><small>PDF</small><b>Enabled</b></article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_results() -> None:
    """Render persisted prediction output when one is available."""
    result: PredictionResult | None = st.session_state.get("prediction")
    st.markdown('<div id="results"></div>', unsafe_allow_html=True)
    if result is None:
        _render_empty_results()
        return

    description = st.session_state["prediction_description"]
    image_bytes = st.session_state["prediction_image"]
    timestamp = st.session_state["prediction_timestamp"]

    st.markdown(
        """
        <div class="section-heading results-heading">
          <span>Analysis complete</span>
          <h2>Your price estimate is ready.</h2>
          <p>A transparent view of the model output and supplied signals.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    usd_col, inr_col, model_col, time_col = st.columns(4, gap="medium")
    with usd_col:
        st.markdown(
            f"""
            <section class="result-stat result-stat-primary">
              <div class="result-stat-icon">$</div>
              <span>Predicted Price</span>
              <strong>${result.usd:,.2f}</strong>
              <small>USD model estimate</small>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with inr_col:
        st.markdown(
            f"""
            <section class="result-stat">
              <div class="result-stat-icon">IN</div>
              <span>Approximate INR</span>
              <strong>INR {result.inr:,.0f}</strong>
              <small>Indicative conversion</small>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with model_col:
        st.markdown(
            f"""
            <section class="result-stat">
              <div class="result-stat-icon">ML</div>
              <span>Model</span>
              <strong class="compact-result">{html.escape(result.model_name)}</strong>
              <small>Preserved backend pipeline</small>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with time_col:
        st.markdown(
            f"""
            <section class="result-stat">
              <div class="result-stat-icon">TS</div>
              <span>Prediction Time</span>
              <strong>{result.elapsed_seconds:.2f}s</strong>
              <small>Inference runtime</small>
            </section>
            """,
            unsafe_allow_html=True,
        )

    image_col, text_col = st.columns([0.38, 0.62], gap="large")
    with image_col:
        st.markdown(
            '<div class="result-panel-label">Analyzed Product</div>',
            unsafe_allow_html=True,
        )
        st.image(image_bytes, width="stretch")
    with text_col:
        st.markdown(
            f"""
            <section class="result-detail-card">
              <div class="result-label">Prediction Summary</div>
              <h3>Multimodal pricing analysis</h3>
              <p>{html.escape(result.summary)}</p>
              <div class="result-detail-grid">
                <div><span>Generated</span><b>{html.escape(timestamp)}</b></div>
                <div><span>Feature vector</span><b>51,282 fused features</b></div>
                <div><span>Currency note</span><b>USD to indicative INR</b></div>
                <div><span>Report</span><b>PDF export ready</b></div>
              </div>
              <div class="model-pill">No fabricated confidence score</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("View product description"):
            st.write(description)
        report = build_prediction_pdf(result, description, timestamp)
        st.download_button(
            "Download PDF Report  ->",
            data=report,
            file_name="pricevision-prediction-report.pdf",
            mime="application/pdf",
            width="stretch",
            type="primary",
        )
    st.caption(
        "The INR value is an approximate currency conversion from the "
        "predicted USD price. PriceVision AI provides estimates, not quotes."
    )
