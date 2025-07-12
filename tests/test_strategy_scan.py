from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.backend.main import app
from app.backend.database.connection import get_db
from app.backend.services import scan as scan_service


from app.backend.database.connection import Base
from app.backend.models.stock import Stock
from app.backend.rules.parser import load_strategy, strategy_to_filters
from app.backend.repositories.stock_repository import StockRepository


def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all([
        Stock(ticker="AAPL", pe_ratio=18, debt_to_equity=0.5, revenue_growth=0.1, market_cap=2500000000000),
        Stock(ticker="TSLA", pe_ratio=70, debt_to_equity=2.0, revenue_growth=0.3, market_cap=800000000000),
        Stock(ticker="PLTR", pe_ratio=45, debt_to_equity=0.2, revenue_growth=0.4, market_cap=50000000000),
    ])
    db.commit()
    return db

def override_get_db(session):
    def _override():
        try:
            yield session
        finally:
            pass
    return _override



def test_strategy_parsing():
    strategy = load_strategy("buffett")
    filters = strategy_to_filters(strategy)
    assert len(filters) == 2


def test_query_generation():
    db = setup_in_memory_db()
    strategy = load_strategy("wood")
    filters = strategy_to_filters(strategy)
    repo = StockRepository(db)
    results = repo.scan(filters, patterns=None)
    tickers = [s.ticker for s in results]
    assert "TSLA" in tickers and "PLTR" in tickers
    assert "AAPL" not in tickers




def test_scan_route_with_patterns():
    db = setup_in_memory_db()

    app.dependency_overrides[get_db] = override_get_db(db)
    client = TestClient(app)

    def fake_get_price_data(ticker, start, end):
        df = pd.DataFrame({"open": [1], "high": [1], "low": [1], "close": [1]})
        df.ticker = ticker
        return df

    def fake_check(df, pattern):
        return getattr(df, "ticker", "") == "AAPL"

    with patch.object(scan_service, "get_price_data", side_effect=fake_get_price_data), \
         patch.object(scan_service, "_check_pattern", side_effect=fake_check):
        res = client.post("/scan/", params={"strategy_id": "buffett", "patterns": "CDLTEST"})

    assert res.status_code == 200
    data = res.json()["results"]
    assert len(data) == 1
    assert data[0]["ticker"] == "AAPL"
