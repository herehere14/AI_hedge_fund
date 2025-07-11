from sqlalchemy import Column, String, Float
from app.backend.database.connection import Base

class Stock(Base):
    __tablename__ = "stocks"

    ticker = Column(String, primary_key=True)
    pe_ratio = Column(Float)
    debt_to_equity = Column(Float)
    revenue_growth = Column(Float)
    market_cap = Column(Float)