import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.backend.main import app
from app.backend.database.connection import Base, engine, SessionLocal
from app.backend.database.models import Alert
from app.backend.scheduler import scan_job

# Ensure tables exist for tests
Base.metadata.create_all(bind=engine)


def clear_alerts():
    with SessionLocal() as db:
        db.query(Alert).delete()
        db.commit()


def test_scan_creates_alerts():
    clear_alerts()
    client = TestClient(app)
    resp = client.post("/alerts/scan", json={"tickers": ["AAPL", "MSFT"]})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    with SessionLocal() as db:
        assert db.query(Alert).count() == 2


@pytest.mark.asyncio
async def test_scan_job_emails(monkeypatch):
    clear_alerts()
    monkeypatch.setenv("ALERT_TICKERS", "AAPL")
    monkeypatch.setenv("ALERT_EMAIL_TO", "test@example.com")
    monkeypatch.setenv("SES_FROM_ADDRESS", "from@example.com")
    with patch("app.backend.services.email.send_email") as mock_email:
        await scan_job()
        assert mock_email.call_count == 1
        with SessionLocal() as db:
            alerted = db.query(Alert).first()
            assert alerted.emailed is True
