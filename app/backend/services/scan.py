from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Dict, Optional

import pandas as pd
from sqlalchemy.orm import Session

from app.backend.rules.parser import load_strategy, strategy_to_filters
from app.backend.repositories.stock_repository import StockRepository
from src.tools.api import get_price_data

try:
    import talib
except Exception:  # pragma: no cover - optional dependency
    talib = None


def _check_pattern(df: pd.DataFrame, pattern: str) -> bool:
    """Return True if the TA-Lib pattern is present on the last row."""
    if talib is None:
        raise RuntimeError("TA-Lib not available")
    func = getattr(talib, pattern, None)
    if func is None:
        raise ValueError(f"Unknown pattern: {pattern}")
    result = func(df["open"], df["high"], df["low"], df["close"])
    if hasattr(result, "iloc"):
        return result.iloc[-1] != 0
    return bool(result[-1])


def scan(strategy_id: str, db: Session, patterns: Optional[List[str]] = None) -> List[Dict[str, List[str]]]:
    """Scan stocks by strategy and optional TA-Lib patterns."""
    strategy = load_strategy(strategy_id)
    filters = strategy_to_filters(strategy)

    repo = StockRepository(db)
    candidates = repo.scan(filters, patterns=None)

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    results: List[Dict[str, List[str]]] = []
    for stock in candidates:
        reasons: List[str] = []
        for rule in strategy.get("filters", []):
            field = rule["field"]
            op = rule["op"]
            val = rule["value"]
            stock_val = getattr(stock, field)
            reasons.append(f"{field} {op} {val} (actual: {stock_val})")

        if patterns:
            df = get_price_data(stock.ticker, start_date, end_date)
            matched = []
            for pat in patterns:
                if _check_pattern(df, pat):
                    matched.append(pat)
            if len(matched) != len(patterns):
                continue
            reasons.extend([f"pattern {p} detected" for p in matched])

        results.append({"ticker": stock.ticker, "reasons": reasons})

    return results


# Backwards compatibility for alerts service
def scan_market(tickers: List[str]) -> List[Dict[str, str]]:
    """Simple alert generation used by alerts endpoints."""
    return [{"ticker": t, "message": f"Generated alert for {t}"} for t in tickers]
