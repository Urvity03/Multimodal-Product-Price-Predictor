# Multimodal Product Price Predictor

## Problem Statement

Build a machine learning solution to predict product prices using multimodal inputs, including product images and product descriptions. The model should combine visual and textual features to improve pricing accuracy for e-commerce products.

## Planned Architecture

- `data/raw/` - store raw datasets and source assets
- `data/processed/` - store cleaned and preprocessed datasets
- `data/images/` - store product images for feature extraction
- `src/data_preprocessing.py` - data cleaning and preprocessing utilities
- `src/image_features.py` - image feature extraction and embedding generation
- `src/text_features.py` - text feature extraction and embedding generation
- `src/train.py` - model training pipeline and evaluation
- `src/predict.py` - inference utilities and prediction pipeline
- `app/app.py` - application entrypoint for serving predictions
- `models/` - store trained model artifacts
- `outputs/plots/` - visualizations and charts
- `outputs/reports/` - evaluation reports and summaries

## Tech Stack

- Python 3.x
- pandas, NumPy, scikit-learn
- PyTorch or TensorFlow
- OpenCV / Pillow
- Jupyter Notebooks
- Flask or FastAPI
