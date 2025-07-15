import os
import pickle


class Cache:
    """Cache for API responses that persists to disk."""

    def __init__(self, filename: str = "cache.pkl"):
        self.filename = filename
        data = self._load_from_file()

        self._prices_cache: dict[str, list[dict[str, any]]] = data.get("prices", {})
        self._financial_metrics_cache: dict[str, list[dict[str, any]]] = data.get(
            "financial_metrics", {}
        )
        self._line_items_cache: dict[str, list[dict[str, any]]] = data.get(
            "line_items", {}
        )
        self._insider_trades_cache: dict[str, list[dict[str, any]]] = data.get(
            "insider_trades", {}
        )
        self._company_news_cache: dict[str, list[dict[str, any]]] = data.get(
            "company_news", {}
        )

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _load_from_file(self) -> dict:
        """Load cache data from disk if available."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "rb") as f:
                    return pickle.load(f)
            except Exception:
                # If loading fails, start with empty cache
                return {}
        return {}

    def _save_to_file(self) -> None:
        """Write the entire cache to disk."""
        data = {
            "prices": self._prices_cache,
            "financial_metrics": self._financial_metrics_cache,
            "line_items": self._line_items_cache,
            "insider_trades": self._insider_trades_cache,
            "company_news": self._company_news_cache,
        }
        try:
            with open(self.filename, "wb") as f:
                pickle.dump(data, f)
        except Exception:
            pass

    def _merge_data(self, existing: list[dict] | None, new_data: list[dict], key_field: str) -> list[dict]:
        """Merge existing and new data, avoiding duplicates based on a key field."""
        if not existing:
            return new_data

        # Create a set of existing keys for O(1) lookup
        existing_keys = {item[key_field] for item in existing}

        # Only add items that don't exist yet
        merged = existing.copy()
        merged.extend([item for item in new_data if item[key_field] not in existing_keys])
        return merged

    def get_prices(self, ticker: str) -> list[dict[str, any]] | None:
        """Get cached price data if available."""
        return self._prices_cache.get(ticker)

    def set_prices(self, ticker: str, data: list[dict[str, any]]):
        """Append new price data to cache."""
        self._prices_cache[ticker] = self._merge_data(
            self._prices_cache.get(ticker), data, key_field="time"
        )
        self._save_to_file()

    def get_financial_metrics(self, ticker: str) -> list[dict[str, any]]:
        """Get cached financial metrics if available."""
        return self._financial_metrics_cache.get(ticker)

    def set_financial_metrics(self, ticker: str, data: list[dict[str, any]]):
        """Append new financial metrics to cache."""
        self._financial_metrics_cache[ticker] = self._merge_data(
            self._financial_metrics_cache.get(ticker),
            data,
            key_field="report_period",
        )
        self._save_to_file()

    def get_line_items(self, ticker: str) -> list[dict[str, any]] | None:
        """Get cached line items if available."""
        return self._line_items_cache.get(ticker)

    def set_line_items(self, ticker: str, data: list[dict[str, any]]):
        """Append new line items to cache."""
        self._line_items_cache[ticker] = self._merge_data(
            self._line_items_cache.get(ticker), data, key_field="report_period"
        )
        self._save_to_file()

    def get_insider_trades(self, ticker: str) -> list[dict[str, any]] | None:
        """Get cached insider trades if available."""
        return self._insider_trades_cache.get(ticker)

    def set_insider_trades(self, ticker: str, data: list[dict[str, any]]):
        """Append new insider trades to cache."""
        self._insider_trades_cache[ticker] = self._merge_data(
            self._insider_trades_cache.get(ticker),
            data,
            key_field="filing_date",
        )  # Could also use transaction_date if preferred
        self._save_to_file()

    def get_company_news(self, ticker: str) -> list[dict[str, any]] | None:
        """Get cached company news if available."""
        return self._company_news_cache.get(ticker)

    def set_company_news(self, ticker: str, data: list[dict[str, any]]):
        """Append new company news to cache."""
        self._company_news_cache[ticker] = self._merge_data(
            self._company_news_cache.get(ticker), data, key_field="date"
        )
        self._save_to_file()


# Global cache instance
_cache: Cache | None = None


def get_cache() -> Cache:
    """Get the global cache instance."""
    global _cache
    if _cache is None:
        _cache = Cache()
    return _cache