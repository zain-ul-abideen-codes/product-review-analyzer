# Import FastAPI TestClient
from fastapi.testclient import TestClient

# Import our FastAPI application
from api.main import app


# Create a test client for the API
client = TestClient(app)


# Test 1 — Health endpoint
def test_health_endpoint():

    # Send GET request to /health
    response = client.get("/health")

    # API should return HTTP 200
    assert response.status_code == 200

    # Check the response content
    assert response.json() == {
        "status": "ok"
    }


# Test 2 — Analyze endpoint accepts a valid review
def test_analyze_valid_review():

    # Send a valid product review
    response = client.post(
        "/analyze",
        json={
            "review": "This memory card works great and is very fast."
        }
    )

    # API should return HTTP 200
    assert response.status_code == 200


# Test 3 — Sentiment field exists
def test_sentiment_field_exists():

    # Send a review to the API
    response = client.post(
        "/analyze",
        json={
            "review": "Excellent product and amazing quality."
        }
    )

    # Convert response to JSON
    result = response.json()

    # Check that sentiment exists
    assert "sentiment" in result


# Test 4 — Topic field exists
def test_topic_field_exists():

    # Send a review to the API
    response = client.post(
        "/analyze",
        json={
            "review": "The delivery was very fast."
        }
    )

    # Convert response to JSON
    result = response.json()

    # Check that topic exists
    assert "topic" in result


# Test 5 — Original review is returned
def test_original_review_returned():

    # Create a test review
    review = "This product works perfectly."

    # Send review to API
    response = client.post(
        "/analyze",
        json={
            "review": review
        }
    )

    # Convert response to JSON
    result = response.json()

    # Check that original review is returned
    assert result["review"] == review


# Test 6 — Sentiment has a valid value
def test_valid_sentiment():

    # Send a review
    response = client.post(
        "/analyze",
        json={
            "review": "I love this product. It works perfectly."
        }
    )

    # Get JSON result
    result = response.json()

    # Allowed sentiment classes
    valid_sentiments = [
        "Positive",
        "Neutral",
        "Negative"
    ]

    # Check predicted sentiment
    assert result["sentiment"] in valid_sentiments


# Test 7 — Topic has a valid value
def test_valid_topic():

    # Send a review
    response = client.post(
        "/analyze",
        json={
            "review": "The package arrived safely."
        }
    )

    # Get JSON result
    result = response.json()

    # Allowed topic classes
    valid_topics = [
        "Packaging",
        "Delivery",
        "Customer Service",
        "Price",
        "Performance / Compatibility",
        "Quality",
        "Other"
    ]

    # Check predicted topic
    assert result["topic"] in valid_topics


# Test 8 — Empty review should be rejected
def test_empty_review():

    # Send an empty review
    response = client.post(
        "/analyze",
        json={
            "review": ""
        }
    )

    # API should reject empty input
    assert response.status_code == 422


# Test 9 — Missing review field should be rejected
def test_missing_review_field():

    # Send request without review field
    response = client.post(
        "/analyze",
        json={}
    )

    # Pydantic validation should reject it
    assert response.status_code == 422


# Test 10 — Wrong data type should be rejected
def test_wrong_review_type():

    # Send a number instead of text
    response = client.post(
        "/analyze",
        json={
            "review": 12345
        }
    )

    # API should reject invalid data
    assert response.status_code == 422