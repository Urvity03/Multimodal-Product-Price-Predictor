# 💰 PriceVision AI

<p align="center">
  <img src="assets/hero_banner.png" alt="PriceVision AI Banner" width="100%">
</p>

<h3 align="center">
AI-Powered Multimodal Product Price Estimation
</h3>

<p align="center">
Estimate product prices using product descriptions, images, and structured attributes through a multimodal machine learning pipeline.
</p>

---

## ✨ Overview

PriceVision AI is a portfolio-grade multimodal machine learning application that estimates product prices by combining **Natural Language Processing**, **Computer Vision**, and **Machine Learning**.

Unlike traditional pricing systems that rely on predefined rules, PriceVision AI learns pricing patterns from product descriptions, images, and structured product attributes to generate intelligent market price estimates.

The application provides:

- 💵 Estimated Market Price (USD)
- 🇮🇳 Approximate INR Conversion
- 📄 Downloadable PDF Report
- 🎨 Premium Responsive Streamlit Interface
- ⚡ Fast Cached Inference Pipeline

---

# 🚀 Features

- 🎯 Multimodal AI price estimation
- 📝 Product description analysis using TF-IDF
- 🖼️ Image feature extraction using EfficientNetB0
- 📦 Structured feature extraction (weight, pack size)
- ⚡ Optimized XGBoost regression model
- 💰 USD prediction with approximate INR conversion
- 📄 Downloadable PDF report
- 🎨 Modern responsive Streamlit interface
- 🚀 Cached model loading for faster predictions

---

# 🏗️ Inference Architecture

```text
                 Product Description
                          │
                          ▼
                 TF-IDF (50,000 Features)

Product Image ─────► EfficientNetB0 (1,280 Features)

Structured Attributes
(weight, quantity, pack size)
                          │
                          ▼
              Feature Fusion (51,282 Features)
                          │
                          ▼
                 Optimized XGBoost Model
                          │
                          ▼
              Estimated Market Price (USD)
                          │
                          ▼
                Approximate INR Conversion
```

---

# 📂 Project Structure

```text
PriceVision-AI
│
├── app/                 # Streamlit application
├── backend/             # Model loading & inference
├── components/          # Reusable UI components
├── assets/              # Logo & hero banner
├── data/                # Model and runtime dataset
├── notebooks/           # Model development
├── src/                 # Research utilities
├── styles/              # Central design system
├── requirements.txt
└── README.md
```

---

# ⚙️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Frontend | Streamlit |
| NLP | TF-IDF |
| Computer Vision | TensorFlow, EfficientNetB0 |
| Machine Learning | XGBoost |
| Image Processing | Pillow |
| Data Processing | Pandas, NumPy |
| Utilities | Joblib, Scikit-learn |

---

# ▶️ Run Locally

Clone the repository

```bash
git clone https://github.com/Urvity03/Multimodal-Product-Price-Predictor.git
```

Move into the project directory

```bash
cd Multimodal-Product-Price-Predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app/app.py
```

The first prediction may take a little longer while EfficientNetB0 and the TF-IDF vocabulary are initialized. Subsequent predictions are significantly faster due to resource caching.

---

# 🤖 Model Information

| Component | Purpose |
|-----------|---------|
| TF-IDF | Product description features |
| EfficientNetB0 | Image feature extraction |
| Regex Feature Engineering | Weight & pack size extraction |
| XGBoost | Final price estimation |

The deployed application reconstructs the TF-IDF vocabulary deterministically from the original ordered corpus to preserve compatibility with the trained XGBoost model. The price prediction model itself is **not retrained during inference**.

---

# ℹ️ Prediction Scope

This model was trained on a broad e-commerce dataset. Predictions are generally more reliable for products similar to those represented in the training data. Estimates for premium, newly released, or rare products may be less accurate.

The deployed model was trained on approximately **5,000 curated e-commerce products** combining **product descriptions, images, and structured attributes**.

---

# 📊 Performance

**Model:** Optimized Multimodal XGBoost

**Mean Absolute Error (MAE):** **13.86**

Predictions are intended as intelligent market estimates rather than exact retail prices.

---

# 🔮 Future Improvements

- Category-specific pricing models
- Brand-aware feature engineering
- Live exchange-rate API
- Multi-currency support
- Confidence calibration
- Cloud deployment
- Model retraining on larger multimodal datasets

---

# 📸 Application Preview

> Screenshots of the application interface will be added after the final UI polish and deployment.

---

# 👩‍💻 Developer

**Urvi Tyagi**

Final Year B.Tech (Artificial Intelligence & Machine Learning)

GitHub:
https://github.com/Urvity03

LinkedIn:
https://www.linkedin.com/in/urvi-tyagi-17b302286/

Project Repository:
https://github.com/Urvity03/Multimodal-Product-Price-Predictor

---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub. It helps others discover the project and supports future improvements.

---

## 📜 License

This project is licensed under the MIT License.
