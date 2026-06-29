"""Landing-page hero component."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from components.navbar import image_data_uri

HERO_IMAGE = Path(__file__).resolve().parent.parent / "assets" / "hero_banner.png"


def render_hero() -> None:
    """Render the hero copy and product illustration."""
    hero_uri = image_data_uri(HERO_IMAGE)
    st.markdown('<div id="home"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <section class="hero-section" aria-label="PriceVision AI overview">
          <div class="hero-copy-block">
            <div class="eyebrow">
              <span class="spark-icon" aria-hidden="true"></span>
              AI-powered price intelligence
            </div>
            <h1 class="hero-title">
              Smarter product pricing through <span>multimodal AI.</span>
            </h1>
            <p class="hero-copy">
              Combine product descriptions, images, and structured signals to
              generate accurate, real-time price estimates.
            </p>
            <div class="hero-actions">
              <a class="hero-primary" href="#predict">
                <span aria-hidden="true"></span> Start Predicting <b>-></b>
              </a>
              <a class="hero-secondary" href="#architecture">
                Learn More <b>v</b>
              </a>
            </div>
            <div class="model-pills" aria-label="Model technologies">
              <span><i class="pill-dot tensorflow"></i>EfficientNetB0</span>
              <span><i class="pill-dot tfidf"></i>TF-IDF</span>
              <span><i class="pill-dot xgboost"></i>XGBoost</span>
              <b>51,282 Features</b>
            </div>
          </div>
          <div class="hero-art-shell">
            <span class="hero-orb orb-one"></span>
            <span class="hero-orb orb-two"></span>
            <span class="hero-orb orb-three"></span>
            <div class="hero-device">
              <div class="hero-visual">
                <img src="{hero_uri}" alt="Multimodal pricing interface">
              </div>
            </div>
            <div class="hero-mini-card hero-price-card">
              <small>Price Estimate</small>
              <strong>$28.75</strong>
              <div class="mini-chart"><i></i><i></i><i></i><i></i></div>
            </div>
            <div class="hero-mini-card hero-image-card">
              <small>Product Image</small>
              <div class="shoe-chip"></div>
            </div>
            <div class="hero-mini-card hero-desc-card">
              <small>Product Description</small>
              <span></span><span></span><span></span>
            </div>
            <div class="hero-mini-card hero-attr-card">
              <small>Attributes</small>
              <p><b>Brand</b><i></i></p>
              <p><b>Material</b><i></i></p>
              <p><b>Pack Size</b><i></i></p>
              <p><b>Category</b><i></i></p>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
