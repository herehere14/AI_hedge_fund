from fastapi import APIRouter, HTTPException

from app.backend.services import backtest as backtest_service

router = APIRouter(prefix="/backtest")


@router.get("/")
async def run_backtest(id: str, years: int = 10):
    """Run a backtest for the given strategy id and number of years."""
    try:
        result = backtest_service.run_backtest(id, years)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))