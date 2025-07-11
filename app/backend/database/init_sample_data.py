from sqlalchemy.orm import Session
from app.backend.models.stock import Stock


def load_sample_data(db: Session):
    if db.query(Stock).count() > 0:
        return
    samples = [
        Stock(ticker="AAPL", pe_ratio=18.0, debt_to_equity=0.5, revenue_growth=0.1, market_cap=2500000000000),
        Stock(ticker="TSLA", pe_ratio=70.0, debt_to_equity=2.0, revenue_growth=0.3, market_cap=800000000000),
        Stock(ticker="PLTR", pe_ratio=45.0, debt_to_equity=0.2, revenue_growth=0.4, market_cap=50000000000),
    ]
    db.add_all(samples)
    db.commit()