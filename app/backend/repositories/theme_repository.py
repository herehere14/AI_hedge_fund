from sqlalchemy.orm import Session
from app.backend.database.models import ThemeIndex


class ThemeRepository:
    """Repository for ThemeIndex operations."""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, doc_id: str, ticker: str, embed_vec: list[float]) -> ThemeIndex:
        obj = self.db.get(ThemeIndex, doc_id)
        if obj:
            obj.ticker = ticker
            obj.embed_vec = embed_vec
        else:
            obj = ThemeIndex(doc_id=doc_id, ticker=ticker, embed_vec=embed_vec)
            self.db.add(obj)
        self.db.commit()
        return obj

    def all(self) -> list[ThemeIndex]:
        return self.db.query(ThemeIndex).all()
