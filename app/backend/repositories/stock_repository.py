from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from app.backend.models.stock import Stock


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def scan(self, filters: List, patterns: List[str] | None = None) -> List[Stock]:
        query = self.db.query(Stock)
        if patterns:
            pattern_filter = [Stock.ticker.ilike(p) for p in patterns]
            query = query.filter(or_(*pattern_filter))
        if filters:
            query = query.filter(*filters)
        return query.all()