# Import Streamlit for building the web interface
import streamlit as st

# Import requests for communicating with FastAPI
import requests


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Product Review Analyzer",
    page_icon="🛍️",
    layout="centered"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    .result-label {
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .result-value {
        font-size: 22px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="title">🛍️ Product Review Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze customer reviews using Machine Learning'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Review Input
# -----------------------------

st.subheader("Enter Product Review")

review = st.text_area(
    "Write your customer review below:",
    placeholder="Example: This memory card works great and is very fast.",
    height=180
)


# -----------------------------
# Analyze Button
# -----------------------------

analyze_button = st.button(
    "🔍 Analyze Review",
    use_container_width=True
)


# -----------------------------
# API Request
# -----------------------------

if analyze_button:

    # Check whether the user entered a review
    if not review.strip():

        st.warning(
            "Please enter a product review first."
        )

    else:

        # FastAPI endpoint
        api_url = "http://127.0.0.1:8000/analyze"

        # Data to send to FastAPI
        payload = {
            "review": review
        }

        try:

            # Send review to FastAPI
            response = requests.post(
                api_url,
                json=payload
            )

            # Check if API request was successful
            if response.status_code == 200:

                # Convert JSON response into Python dictionary
                result = response.json()

                # Get sentiment prediction
                sentiment = result["sentiment"]

                # Get topic prediction
                topic = result["topic"]

                # -----------------------------
                # Display Results
                # -----------------------------

                st.success(
                    "Review analyzed successfully!"
                )

                st.markdown("### Analysis Result")

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        '<div class="result-box">',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '<div class="result-label">SENTIMENT</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="result-value">{sentiment}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                with col2:

                    st.markdown(
                        '<div class="result-box">',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '<div class="result-label">TOPIC</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="result-value">{topic}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

            else:

                st.error(
                    "API returned an error. Please check the FastAPI server."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI. "
                "Please make sure the API server is running."
            )

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )


# -----------------------------
# Footer
# -----------------------------

st.markdown("---")

st.caption(
    "Product Review Sentiment & Topic Analyzer | "
    "Machine Learning + FastAPI + Streamlit"
)