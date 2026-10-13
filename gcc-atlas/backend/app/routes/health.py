"""
Health check route for GCC Atlas
"""

from fastapi import APIRouter
from app.config import settings
from app.database import query_one
from app.models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Verify backend and database connectivity."""
    db_ok = False
    comp_count = 0
    city_count = 0
    try:
        row = query_one("SELECT COUNT(*) as c FROM companies")
        if row:
            comp_count = row["c"]
            db_ok = True
        city_row = query_one("SELECT COUNT(*) as c FROM cities")
        if city_row:
            city_count = city_row["c"]
    except Exception:
        db_ok = False

    ai_mode = "live_llm" if settings.gemini_api_key else "demo_mode"

    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        version=settings.version,
        database_connected=db_ok,
        total_companies=comp_count,
        total_cities=city_count,
        ai_mode=ai_mode
    )
