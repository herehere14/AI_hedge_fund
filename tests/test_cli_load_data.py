import types
from click.testing import CliRunner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.database.connection import Base
from app.backend.database.models import Fundamentals
from app.backend.cli import load_data


def setup_memory_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    monkeypatch.setattr(load_data, "engine", engine)
    monkeypatch.setattr(load_data, "SessionLocal", Session)
    return Session


def test_load_fundamentals(monkeypatch):
    Session = setup_memory_db(monkeypatch)

    class DummyTicker:
        info = {
            "returnOnEquity": 0.1,
            "trailingPE": 15.0,
            "pegRatio": 1.2,
            "profitMargins": 0.3,
        }

    monkeypatch.setattr(load_data, "yf", types.SimpleNamespace(Ticker=lambda t: DummyTicker()))

    runner = CliRunner()
    result = runner.invoke(load_data.cli, ["load-fundamentals", "--ticker", "AAPL"])
    assert result.exit_code == 0

    with Session() as session:
        row = session.query(Fundamentals).filter_by(ticker="AAPL").first()
        assert row is not None
        assert row.pe == 15.0
