from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.rules.parser import load_strategy, strategy_to_filters
from app.backend.repositories.stock_repository import StockRepository
from app.backend.models.stock import Stock

router = APIRouter(prefix="/scan", tags=["scan"])


@router.post("/")
async def scan_stocks(strategy_id: str, patterns: Optional[List[str]] = None, db: Session = Depends(get_db)):
    try:
        strategy = load_strategy(strategy_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Strategy not found")

    filters = strategy_to_filters(strategy)
    repo = StockRepository(db)
    stocks = repo.scan(filters, patterns)

    results = []
    for stock in stocks:
        reasons = []
        for f in strategy.get('filters', []):
            field = f['field']
            op = f['op']
            val = f['value']
            stock_val = getattr(stock, field)
            reasons.append(f"{field} {op} {val} (actual: {stock_val})")
        results.append({"ticker": stock.ticker, "reasons": reasons})

    return {"results": results}