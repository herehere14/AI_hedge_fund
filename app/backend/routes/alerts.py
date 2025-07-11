from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.backend.database import get_db
from app.backend.repositories.alert_repository import AlertRepository
from app.backend.models.schemas import ScanRequest, AlertResponse
from app.backend.services.scan import scan_market

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("/scan", response_model=List[AlertResponse])
async def scan(request: ScanRequest, db: Session = Depends(get_db)):
    matches = scan_market(request.tickers)
    repo = AlertRepository(db)
    alerts = [repo.create_alert(m["ticker"], m["message"]) for m in matches]
    return alerts