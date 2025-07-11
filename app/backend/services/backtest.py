import pandas as pd
import math
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import yfinance as yf

import vectorbt as vbt


def _fetch_price_data(symbol: str, years: int) -> pd.Series:
    end = pd.Timestamp.today()
    start = end - pd.DateOffset(years=years)
    data = yf.download(symbol, start=start, end=end, progress=False)
    if "Close" not in data:
        raise ValueError("No close prices returned")
    return data["Close"].dropna()


def _run_sma_strategy(price_series: pd.Series) -> vbt.Portfolio:
    fast_ma = vbt.MA.run(price_series, window=20)
    slow_ma = vbt.MA.run(price_series, window=50)
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    pf = vbt.Portfolio.from_signals(price_series, entries, exits, init_cash=10000, freq="1D")
    return pf


def run_backtest(strategy_id: str, years: int = 10, price_data: pd.Series | None = None, symbol: str = "SPY") -> dict:
    if price_data is None:
        price_data = _fetch_price_data(symbol, years)

    if strategy_id.upper() == "STRAT":
        pf = _run_sma_strategy(price_data)
    else:
        raise ValueError(f"Unknown strategy id: {strategy_id}")

    values = pf.value()
    returns = values.pct_change().dropna()
    cagr = (values.iloc[-1] / values.iloc[0]) ** (252 / len(returns)) - 1
    sharpe = math.sqrt(252) * (returns.mean() / returns.std()) if returns.std() != 0 else 0.0

    plt.figure()
    values.plot()
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    encoded_img = base64.b64encode(buf.getvalue()).decode()

    return {"cagr": float(cagr), "sharpe": sharpe, "equity_curve": encoded_img}
