from typing import List, Dict


def scan_market(tickers: List[str]) -> List[Dict[str, str]]:
    """Dummy scan implementation that creates an alert for each ticker."""
    results = []
    for t in tickers:
        results.append({"ticker": t, "message": f"Generated alert for {t}"})
    return results