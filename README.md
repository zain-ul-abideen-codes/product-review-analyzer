# Product Review Sentiment & Topic Analyzer

An end-to-end NLP project that analyzes customer product reviews and predicts:

- **Sentiment:** Positive, Neutral, or Negative
- **Topic:** Packaging, Delivery, Customer Service, Price, Performance / Compatibility, Quality, or Other

Built with **scikit-learn, FastAPI, and Streamlit**.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Models & Results](#models--results)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

Reading thousands of customer reviews manually is slow. This project automatically analyzes a review and returns:

1. How the customer feels about the product (sentiment)
2. What the review is mainly about (topic)

## Features

- Sentiment analysis (3 classes)
- Topic classification (7 classes)
- Shared text-cleaning pipeline for training and inference
- TF-IDF feature extraction + Logistic Regression models
- FastAPI REST API with Pydantic input validation
- Streamlit web interface
- Automated tests with Pytest (10 tests)
- Pre-trained models saved with Joblib

## Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI
  ↓
Text Cleaning
  ↓
Sentiment Model + Topic Model
  ↓
Result
  ↓
Streamlit UI
```

| Layer    | Technology |
| -------- | ---------- |
| Frontend | Streamlit  |
| Backend  | FastAPI    |
| ML       | scikit-learn (TF-IDF + Logistic Regression) |

## Dataset

Amazon product reviews dataset — **4,915 reviews**.

| Column       | Description         |
| ------------ | ------------------- |
| `overall`    | Product rating (1–5) |
| `reviewText` | Customer review text |

### Text Preprocessing

1. Convert to lowercase
2. Remove special characters
3. Remove punctuation
4. Remove extra spaces

## Models & Results

### Sentiment Analysis

**Model:** TF-IDF + Logistic Regression

| Rating   | Label    |
| -------- | -------- |
| >= 4     | Positive |
| == 3     | Neutral  |
| < 3      | Negative |

**Accuracy: 92.27%**

> The dataset is heavily skewed toward Positive reviews, so the model performs better on Positive than on Neutral and Negative.

### Topic Classification

**Model:** TF-IDF + Balanced Logistic Regression

| Metric   | Score  |
| -------- | ------ |
| Accuracy | 72.94% |
| Macro F1 | 0.68   |

The original dataset had no topic labels, so labels were generated with **keyword-based rules (weak labels)**. Scores are measured against these weak labels, not human annotations.

### Training Pipeline

```text
Amazon Reviews
  ↓
Clean Text
  ↓
Create Labels
  ↓
Train/Test Split
  ↓
TF-IDF
  ↓
Logistic Regression
  ↓
Evaluation
  ↓
Save Model
```

## Project Structure

```text
product-review-analyzer/
├── api/
│   ├── __init__.py
│   └── main.py                  # FastAPI app
├── data/
│   ├── processed/
│   └── raw/
│       └── amazon_reviews.csv
├── frontend/
│   └── app.py                   # Streamlit app
├── models/
│   ├── sentiment_model.joblib
│   ├── sentiment_vectorizer.joblib
│   ├── topic_model.joblib
│   └── topic_vectorizer.joblib
├── notebooks/
│   └── 01_data_exploration.ipynb
├── tests/
│   └── test_api.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/product-review-analyzer.git
cd product-review-analyzer
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas scikit-learn joblib fastapi uvicorn streamlit requests pytest httpx
```

### 4. Start the API (Terminal 1)

```bash
uvicorn api.main:app --reload
```

- API: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- Swagger docs: http://127.0.0.1:8000/docs

### 5. Start the frontend (Terminal 2)

Activate the virtual environment again, then:

```bash
streamlit run frontend/app.py
```

Open the local URL shown in the terminal.

### 6. Try it

Enter a review:

```text
This memory card works great and is very fast.
```

Click **Analyze Review**. Output:

```text
Sentiment: Positive
Topic: Performance / Compatibility
```

## API Reference

| Method | Endpoint   | Description              |
| ------ | ---------- | ------------------------ |
| GET    | `/health`  | Check API status         |
| POST   | `/analyze` | Analyze a product review |

**Request**

```json
{
  "review": "This memory card works great and is very fast."
}
```

**Response**

```json
{
  "review": "This memory card works great and is very fast.",
  "sentiment": "Positive",
  "topic": "Performance / Compatibility"
}
```

**Health response**

```json
{
  "status": "ok"
}
```

## Testing

```bash
python -m pytest -v
```

Expected: `10 passed`

Tests cover: API health, review analysis, sentiment and topic results, response fields, valid sentiment/topic values, empty review, missing review, and wrong data type.

## Limitations

- **Class imbalance:** Sentiment performance is weaker on Neutral and Negative classes.
- **Weak topic labels:** Topic labels are keyword-generated, not manually verified.
- **Single topic:** A review may cover multiple topics, but the system returns only one.

## Future Improvements

- [ ] Improve sentiment performance for minority classes
- [ ] Build a manually labeled topic dataset
- [ ] Support multi-label topic prediction
- [ ] Add batch review analysis
- [ ] Add a sentiment dashboard
- [ ] Add PostgreSQL
- [ ] Add Docker
- [ ] Deploy online
