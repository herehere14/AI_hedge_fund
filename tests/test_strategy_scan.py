from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
