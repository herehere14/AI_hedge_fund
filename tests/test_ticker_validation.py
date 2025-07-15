import pytest
from unittest.mock import patch

from src.tools.api import get_prices

@patch('src.tools.api._cache')
@patch('src.tools.api.requests.get')
def test_invalid_ticker_raises_error(mock_get, mock_cache):
    mock_cache.get_prices.return_value = None
    with pytest.raises(ValueError):
        get_prices('INVALID', '2024-01-01', '2024-01-02')
    mock_get.assert_not_called()