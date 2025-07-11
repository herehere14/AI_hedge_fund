from app.backend.database.connection import SessionLocal
from app.backend.database.models import GuruStats


def calculate_cagr(start_value: float, end_value: float, years: float) -> float | None:
    """Calculate Compound Annual Growth Rate."""
    if start_value <= 0 or years <= 0:
        return None
    return (end_value / start_value) ** (1 / years) - 1


def update_guru_stats() -> None:
    """Recalculate CAGR for all guru stats rows and persist results."""
    with SessionLocal() as session:
        stats = session.query(GuruStats).all()
        for stat in stats:
            years = (stat.end_date - stat.start_date).days / 365.0
            stat.cagr = calculate_cagr(stat.start_value, stat.end_value, years)
        session.commit()


if __name__ == "__main__":
    update_guru_stats()