# PriceVision AI

PriceVision AI is a portfolio-grade multimodal product pricing application. It
combines product descriptions, product imagery, and structured package signals
to generate a model-based USD price estimate with an approximate INR conversion
and a downloadable PDF report.

## Product experience

- Premium, responsive Streamlit interface
- Validated description and image upload workflow
- Real-time progress and persistent results dashboard
- USD prediction and approximate INR conversion
- Input summary, model metadata, and local PDF report generation
- Lazy-loaded, cached model components

## Inference architecture

```text
Product description --> TF-IDF (50,000)
Product image -------> EfficientNetB0 (1,280)
Description ---------> Weight + pack size (2)
                                  |
                                  v
                    51,282 fused features
                                  |
                                  v
                     Optimized XGBoost model
                                  |
                                  v
                         USD price estimate
```

The trained XGBoost regressor is preserved. The original notebook did not save
its fitted TF-IDF vectorizer, so the application deterministically reconstructs
the vocabulary from the original ordered `sample_5000.csv` corpus on first use.
That cached vectorizer recreates the exact 50,000-feature contract expected by
the model; the price model itself is not retrained.

## Project structure

```text
app/          Streamlit entry point
assets/       Local logo and hero artwork
backend/      Model loading, preprocessing, inference, and report generation
components/   Reusable interface sections
data/         Preserved model, corpus, and local datasets
notebooks/    Research and model development workflow
src/          Original experimentation utilities
styles/       Central responsive design system
```

## Run locally

Use Python 3.11 in a virtual environment:

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

The first prediction can take longer while EfficientNetB0 and the TF-IDF
vocabulary initialize. Subsequent predictions reuse cached resources.

## Model

| Component | Role |
| --- | --- |
| TF-IDF | Product language features |
| EfficientNetB0 | Visual embeddings |
| Regex feature extraction | Weight and pack size |
| XGBoost | Final log-price regression |

Notebook evaluation recorded an MAE of **13.8603** for the optimized multimodal
model. Predictions are estimates for decision support and may differ from real
market prices.

## Tech stack

Python, Streamlit, TensorFlow/Keras, EfficientNetB0, scikit-learn, SciPy,
XGBoost, and Pillow

## Developer

Built by [Urvity](https://github.com/Urvity03). Source:
[Multimodal Product Price Predictor](https://github.com/Urvity03/Multimodal-Product-Price-Predictor).
