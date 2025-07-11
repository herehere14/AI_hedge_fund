import os
import logging
import requests

logger = logging.getLogger(__name__)

SENTIMENT_API_URL = os.environ.get("SENTIMENT_API_URL", "http://sentiment-api:8000")


def analyze_headline_sentiment(headline: str) -> str | None:
    """Return sentiment label for a headline using the FinBERT REST service."""
    try:
        response = requests.post(
            f"{SENTIMENT_API_URL}/predict",
            json={"text": headline},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            if "label" in data:
                return data["label"]
            if "sentiment" in data:
                return data["sentiment"]
            if "predictions" in data and data["predictions"]:
                pred = data["predictions"][0]
                return pred.get("label") or pred.get("sentiment")
    except Exception as e:
        logger.error("Sentiment API request failed: %s", e)
    return None