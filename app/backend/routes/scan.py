from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.services import scan as scan_service

router = APIRouter(prefix="/scan", tags=["scan"])


@router.post("/")
async def scan_stocks(strategy_id: str, patterns: Optional[List[str]] = None, db: Session = Depends(get_db)):
    try:
        results = scan_service.scan(strategy_id, db, patterns)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"results": results}