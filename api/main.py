# Import FastAPI
from fastapi import FastAPI

# Import Pydantic for request data validation
from pydantic import BaseModel, Field

# Import joblib to load saved ML models
import joblib

# Import regular expressions for text cleaning
import re


# Create the FastAPI application
app = FastAPI(
    title="Product Review Sentiment & Topic Analyzer",
    description="API for analyzing product reviews",
    version="1.0.0"
)


# Load the trained sentiment model
sentiment_model = joblib.load(
    "models/sentiment_model.joblib"
)

# Load the sentiment TF-IDF vectorizer
sentiment_vectorizer = joblib.load(
    "models/sentiment_vectorizer.joblib"
)

# Load the trained topic model
topic_model = joblib.load(
    "models/topic_model.joblib"
)

# Load the topic TF-IDF vectorizer
topic_vectorizer = joblib.load(
    "models/topic_vectorizer.joblib"
)


# Clean review text in the same way as during model training
def clean_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and punctuation
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text).strip()

    # Return the cleaned text
    return text


# Define the structure of the API request
class ReviewRequest(BaseModel):

    # Review must be text and contain at least 1 character
    review: str = Field(min_length=1)


# Health check endpoint
@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


# Analyze a single product review
@app.post("/analyze")
def analyze_review(request: ReviewRequest):

    # Get the review sent by the user
    review_text = request.review

    # Clean the review text
    cleaned_review = clean_text(review_text)

    # Convert cleaned review into TF-IDF features for sentiment model
    sentiment_features = sentiment_vectorizer.transform(
        [cleaned_review]
    )

    # Predict sentiment
    sentiment_prediction = sentiment_model.predict(
        sentiment_features
    )[0]

    # Convert cleaned review into TF-IDF features for topic model
    topic_features = topic_vectorizer.transform(
        [cleaned_review]
    )

    # Predict topic
    topic_prediction = topic_model.predict(
        topic_features
    )[0]

    # Return the analysis result as JSON
    return {
        "review": review_text,
        "sentiment": sentiment_prediction,
        "topic": topic_prediction
    }