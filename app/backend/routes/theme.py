from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import numpy as np

from app.backend.database.connection import get_db
from app.backend.repositories.theme_repository import ThemeRepository
from app.backend.services.embedding import embed_query
from app.backend.models.schemas import ThemeSearchResponse

router = APIRouter()


@router.get("/theme", response_model=ThemeSearchResponse)
def theme_search(
    query: str = Query(..., description="Search text"),
    top_k: int = Query(5, ge=1, le=50, description="Number of tickers to return"),
    db: Session = Depends(get_db),
) -> ThemeSearchResponse:
    qvec = np.array(embed_query(query))
    repo = ThemeRepository(db)
    items = repo.all()
    scored = sorted(
        items,
        key=lambda item: float(np.linalg.norm(np.array(item.embed_vec) - qvec)),
    )
    return ThemeSearchResponse(tickers=[item.ticker for item in scored[:top_k]])
