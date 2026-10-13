"""
Dashboard intelligence routes for GCC Atlas
Computes all KPI totals, breakdowns, and recent milestones dynamically from SQLite.
"""

from fastapi import APIRouter
from app.database import query_all, query_one
from app.models import (
    DashboardResponse,
    SectorDistributionItem,
    CityDistributionItem,
    ExpansionItem,
    CompanyBase
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard_data():
    """Retrieve dynamic KPIs, distributions, and recent announcements."""
    # 1. Total counts
    comp_row = query_one("SELECT COUNT(*) as count FROM companies")
    total_companies = comp_row["count"] if comp_row else 0

    city_row = query_one("SELECT COUNT(*) as count FROM cities")
    total_cities = city_row["count"] if city_row else 0

    sector_row = query_one("SELECT COUNT(DISTINCT sector) as count FROM companies")
    total_sectors = sector_row["count"] if sector_row else 0

    source_row = query_one("SELECT COUNT(*) as count FROM sources")
    total_sources = source_row["count"] if source_row else 0

    # 2. Sector distribution
    sector_rows = query_all("""
        SELECT sector, COUNT(*) as count
        FROM companies
        GROUP BY sector
        ORDER BY count DESC
    """)
    sector_distribution = []
    for r in sector_rows:
        cnt = r["count"]
        pct = round((cnt / total_companies * 100), 1) if total_companies > 0 else 0.0
        sector_distribution.append(SectorDistributionItem(
            sector=r["sector"],
            count=cnt,
            percentage=pct
        ))

    # 3. City distribution
    city_rows = query_all("""
        SELECT city_name, COUNT(*) as count
        FROM companies
        GROUP BY city_name
        ORDER BY count DESC
    """)
    city_distribution = []
    for r in city_rows:
        cnt = r["count"]
        pct = round((cnt / total_companies * 100), 1) if total_companies > 0 else 0.0
        city_distribution.append(CityDistributionItem(
            city_name=r["city_name"],
            count=cnt,
            percentage=pct
        ))

    # 4. Recent companies added / updated
    recent_comp_rows = query_all("""
        SELECT * FROM companies
        ORDER BY last_verified_date DESC, name ASC
        LIMIT 6
    """)
    recent_companies = [CompanyBase(**r) for r in recent_comp_rows]

    # 5. Recent expansions
    exp_rows = query_all("""
        SELECT * FROM expansions
        ORDER BY date DESC
        LIMIT 5
    """)
    recent_expansions = [ExpansionItem(**r) for r in exp_rows]

    prototype_disclaimer = (
        "Dataset Note: GCC Atlas MVP currently indexes a curated dataset of 28 verified multinational Global Capability "
        "Centres across 6 major Indian metropolitan hubs. This prototype serves as a structured intelligence sample and "
        "does not constitute an exhaustive census of all ~1,600+ GCCs operating nationwide."
    )

    return DashboardResponse(
        total_companies=total_companies,
        total_cities=total_cities,
        total_sectors=total_sectors,
        total_sources=total_sources,
        sector_distribution=sector_distribution,
        city_distribution=city_distribution,
        recent_companies=recent_companies,
        recent_expansions=recent_expansions,
        prototype_disclaimer=prototype_disclaimer
    )
