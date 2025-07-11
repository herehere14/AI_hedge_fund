from unittest.mock import Mock, patch

import pytest

from src.tools.api import get_company_news


def sample_news_response():
    return {
        "news": [
            {
                "ticker": "AAPL",
                "title": "Great quarter results",
                "author": "x",
                "source": "y",
                "date": "2024-01-01T00:00:00Z",
                "url": "http://example.com/a",
                "sentiment": None,
            },
            {
                "ticker": "AAPL",
                "title": "Product recall issue",
                "author": "x",
                "source": "y",
                "date": "2024-01-02T00:00:00Z",
                "url": "http://example.com/b",
                "sentiment": "negative",
            },
        ]
    }


class DummyResponse:
    def __init__(self, data):
        self._data = data
        self.status_code = 200

    def json(self):
        return self._data


@patch("src.tools.api._make_api_request")
@patch("app.backend.services.sentiment.analyze_headline_sentiment")
def test_news_sentiment_enrichment(mock_sentiment, mock_request):
    mock_request.return_value = DummyResponse(sample_news_response())
    mock_sentiment.return_value = "positive"

    news = get_company_news("AAPL", "2024-01-02", limit=2)

    assert len(news) == 2
    assert news[0].sentiment == "positive"
    assert news[1].sentiment == "negative"
    mock_sentiment.assert_called_once_with("Great quarter results")
