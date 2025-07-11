import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from httpx import AsyncClient
from .database.connection import SessionLocal
from .repositories import AlertRepository
from .services.email import send_email

scheduler = AsyncIOScheduler()


async def scan_job():
    tickers = os.getenv("ALERT_TICKERS", "AAPL").split(",")
    async with AsyncClient(base_url="http://localhost:8000") as client:
        resp = await client.post("/alerts/scan", json={"tickers": tickers})
        resp.raise_for_status()
        alerts = resp.json()

    # Mark emailed and send notifications
    db = SessionLocal()
    repo = AlertRepository(db)
    to_addr = os.getenv("ALERT_EMAIL_TO")
    for alert in alerts:
        if to_addr:
            send_email(to_addr, f"Alert for {alert['ticker']}", alert['message'])
        repo.mark_emailed(alert["id"])
    db.close()


def start():
    scheduler.add_job(scan_job, "interval", minutes=60, id="scan_job")
    scheduler.start()