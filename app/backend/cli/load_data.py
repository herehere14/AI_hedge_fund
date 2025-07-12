import logging
from datetime import datetime

import click
import pandas as pd
import yfinance as yf
from sqlalchemy.exc import SQLAlchemyError

from app.backend.database.connection import Base, SessionLocal, engine
from app.backend.database.models import Price, Fundamentals

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    """Backend data loading utilities."""
    pass


@cli.command("load-eod")
@click.option("--ticker", required=True, help="Ticker symbol, e.g. BRK-B")
@click.option("--start", required=True, help="Start date YYYY-MM-DD")
@click.option(
    "--end",
    default=datetime.now().strftime("%Y-%m-%d"),
    show_default=True,
    help="End date YYYY-MM-DD",
)
@click.option("--retries", default=3, show_default=True, help="Number of retries")
def load_eod(ticker: str, start: str, end: str, retries: int) -> None:
    """Load historical prices into the database using yfinance."""

    Base.metadata.create_all(bind=engine)

    data = None
    for attempt in range(1, retries + 1):
        try:
            logger.info(
                "Fetching %s data from %s to %s (attempt %s)", ticker, start, end, attempt
            )
            data = yf.download(ticker, start=start, end=end, progress=False)
            if not data.empty:
                break
            logger.warning("Received empty data from yfinance")
        except Exception as e:  # noqa: BLE001
            logger.error("Error fetching data: %s", e)
        if attempt < retries:
            logger.info("Retrying...")
    if data is None or data.empty:
        logger.error("Failed to download data for %s", ticker)
        return

    data.reset_index(inplace=True)
    session = SessionLocal()
    inserted = 0
    try:
        for row in data.itertuples(index=False):
            price = Price(
                ticker=ticker,
                date=row.Date.date() if hasattr(row.Date, "date") else row.Date,
                open=row.Open,
                high=row.High,
                low=row.Low,
                close=row.Close,
                adj_close=getattr(row, "Adj Close"),
                volume=int(row.Volume) if not pd.isna(row.Volume) else None,
            )
            session.merge(price)
            inserted += 1
        session.commit()
        logger.info("Inserted %s rows", inserted)
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("Database error: %s", e)
    finally:
        session.close()


@cli.command("load-fundamentals")
@click.option("--ticker", required=True, help="Ticker symbol")
def load_fundamentals(ticker: str) -> None:
    """Load fundamental metrics using yfinance."""

    Base.metadata.create_all(bind=engine)

    try:
        info = yf.Ticker(ticker).info
    except Exception as e:  # noqa: BLE001
        logger.error("Error fetching fundamentals: %s", e)
        return

    session = SessionLocal()
    try:
        fundamentals = Fundamentals(
            ticker=ticker,
            fiscal_date=datetime.now().date(),
            roe=info.get("returnOnEquity"),
            pe=info.get("trailingPE"),
            peg=info.get("pegRatio"),
            moat_pct=info.get("profitMargins"),
        )
        session.merge(fundamentals)
        session.commit()
        logger.info("Inserted fundamentals for %s", ticker)
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("Database error: %s", e)
    finally:
        session.close()



if __name__ == "__main__":
    cli()