from sqlalchemy.orm import Session
from typing import List
from app.backend.database.models import Alert


class AlertRepository:
    """CRUD operations for alerts."""

    def __init__(self, db: Session):
        self.db = db

    def create_alert(self, ticker: str, message: str) -> Alert:
        alert = Alert(ticker=ticker, message=message)
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_unemailed_alerts(self) -> List[Alert]:
        return self.db.query(Alert).filter(Alert.emailed == False).all()

    def mark_emailed(self, alert_id: int) -> None:
        alert = self.db.query(Alert).get(alert_id)
        if alert:
            alert.emailed = True
            self.db.commit()
            self.db.refresh(alert)