"""Product input and prediction orchestration component."""

from __future__ import annotations

import streamlit as st

from backend.image_utils import ImageValidationError
from backend.model_loader import ModelAssetError
from backend.predict import predict_price
from backend.utils import current_timestamp


@st.cache_data(show_spinner=False, max_entries=32)
def _cached_prediction(description: str, image_bytes: bytes):
    """Cache identical inference requests within the Streamlit session."""
    return predict_price(description, image_bytes)


def render_prediction_form() -> None:
    """Render input controls and store a successful result in session state."""
    st.markdown('<div id="predict"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <section class="workspace-heading">
          <span class="spark-icon" aria-hidden="true"></span>
          <div>
            <h2>New Price Prediction</h2>
            <p>Describe the product, upload its image, and run the preserved multimodal model.</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(
            """
            <div class="workspace-topline">
              <div>
                <span>Prediction Workspace</span>
                <strong>51,282-feature inference pipeline</strong>
              </div>
              <b>Live model</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("prediction_form", clear_on_submit=False):
            text_col, image_col, info_col = st.columns(
                [1.55, 1.05, 0.9],
                gap="medium",
                vertical_alignment="top",
            )
            with text_col:
                st.markdown("#### Product Description")
                st.caption(
                    "Include brand, category, quantity, material, condition, and notable specifications."
                )
                description = st.text_area(
                    "Product description",
                    value=st.session_state.get("draft_description", ""),
                    placeholder=(
                        "Example: Premium stainless-steel insulated bottle, "
                        "750 ml, leak-proof lid, pack of 2..."
                    ),
                    height=220,
                    max_chars=5_000,
                    label_visibility="collapsed",
                )
                st.markdown(
                    f'<div class="input-meta"><span>Minimum 20 characters required</span>'
                    f"<b>{len(description):,} / 5,000</b></div>",
                    unsafe_allow_html=True,
                )

            with image_col:
                st.markdown("#### Product Image")
                st.caption("Upload a clear, well-lit image of the product.")
                st.markdown(
                    """
                    <div class="upload-visual" aria-hidden="true">
                      <span></span>
                      <strong>Drag and drop an image here</strong>
                      <p>or click to browse</p>
                      <small>JPG, PNG, WEBP - Max 10MB</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                uploaded = st.file_uploader(
                    "Upload product image",
                    type=["jpg", "jpeg", "png", "webp"],
                    accept_multiple_files=False,
                    label_visibility="collapsed",
                    help="JPG, PNG, or WebP up to 10 MB",
                )
                if uploaded is not None:
                    st.image(uploaded, caption=uploaded.name, width="stretch")

            with info_col:
                st.markdown(
                    """
                    <aside class="prediction-info" aria-label="Prediction trust panel">
                      <div><i class="info-blue">AI</i><p><b>Real ML Model</b>
                        <span>51,282 features</span></p></div>
                      <div><i class="info-green">OK</i><p><b>Secure</b>
                        <span>Your data is not stored</span></p></div>
                      <div><i class="info-purple">1x</i><p><b>One Prediction</b>
                        <span>Per session run</span></p></div>
                      <hr>
                      <small>Output: USD estimate, INR conversion, inference time, summary, PDF.</small>
                    </aside>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "Generate Price Estimate  ->",
                width="stretch",
                type="primary",
            )
            st.markdown(
                """
                <p class="privacy-note">
                  Inputs are processed only for this prediction workflow.
                </p>
                """,
                unsafe_allow_html=True,
            )

    if not submitted:
        return

    st.session_state["draft_description"] = description
    if uploaded is None:
        st.error("Upload a product image to continue.", icon=":material/warning:")
        return

    image_bytes = uploaded.getvalue()
    progress = st.progress(12, text="Validating product inputs...")
    try:
        progress.progress(32, text="Building language features...")
        with st.spinner("Analyzing text and visual product signals..."):
            result = _cached_prediction(description, image_bytes)
        progress.progress(88, text="Calibrating price estimate...")
        st.session_state["prediction"] = result
        st.session_state["prediction_description"] = description.strip()
        st.session_state["prediction_image"] = image_bytes
        st.session_state["prediction_image_name"] = uploaded.name
        st.session_state["prediction_timestamp"] = current_timestamp()
        progress.progress(100, text="Prediction ready")
        st.toast("Price estimate generated", icon=":material/check_circle:")
    except (ValueError, ImageValidationError, ModelAssetError) as exc:
        st.error(str(exc), icon=":material/warning:")
    except Exception as exc:
        st.error(
            "The prediction pipeline could not complete. "
            f"Technical detail: {exc}",
            icon=":material/warning:",
        )
    finally:
        progress.empty()
