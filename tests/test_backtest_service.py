import types
import sys
import pandas as pd
import pytest


def create_stub_vectorbt():
    module = types.ModuleType("vectorbt")

    class DummyMA:
        def __init__(self, series):
            self.ma = series

        @staticmethod
        def run(series, window):
            ma = series.rolling(window).mean()
            return DummyMA(ma)

        def ma_crossed_above(self, other):
            return self.ma > other.ma

        def ma_crossed_below(self, other):
            return self.ma < other.ma

    class DummyPortfolio:
        def __init__(self, close):
            self._value = (1 + close.pct_change().fillna(0)).cumprod() * 10000

        @staticmethod
        def from_signals(close, entries, exits, init_cash=10000, freq="1D"):
            return DummyPortfolio(close)

        def value(self):
            return self._value

    module.MA = DummyMA
    module.Portfolio = DummyPortfolio
    return module


def setup_module(module):
    stub = create_stub_vectorbt()
    sys.modules["vectorbt"] = stub
    global backtest
    import importlib
    backtest = importlib.import_module("app.backend.services.backtest")


def test_run_backtest_returns_metrics():
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    prices = pd.Series([100 + i * 0.1 for i in range(len(dates))], index=dates)

    result = backtest.run_backtest("STRAT", years=1, price_data=prices)

    assert "cagr" in result
    assert "sharpe" in result
    assert "equity_curve" in result
    assert isinstance(result["equity_curve"], str)


def test_run_backtest_invalid_strategy():
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    prices = pd.Series([100 + i * 0.5 for i in range(len(dates))], index=dates)

    with pytest.raises(ValueError):
        backtest.run_backtest("UNKNOWN", years=1, price_data=prices)
