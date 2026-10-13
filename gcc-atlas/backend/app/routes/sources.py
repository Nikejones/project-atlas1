"""
Sources and data quality intelligence routes for GCC Atlas
"""

from fastapi import APIRouter
from app.database import query_all, query_one
from app.models import SourcesResponse, SourceItem, DataQualityReport

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.get("", response_model=SourcesResponse)
def get_sources_and_quality():
    """Retrieve verified sources catalog and dataset completeness metrics."""
    # 1. Sources with count of linked companies
    source_rows = query_all("""
        SELECT s.*, COUNT(c.id) as linked_company_count
        FROM sources s
        LEFT JOIN companies c ON s.id = c.source_id
        GROUP BY s.id
        ORDER BY linked_company_count DESC, s.name ASC
    """)
    sources = [SourceItem(**r) for r in source_rows]

    # 2. Data quality completeness metrics
    comp_total_row = query_one("SELECT COUNT(*) as total FROM companies")
    total_comps = comp_total_row["total"] if comp_total_row else 0

    year_row = query_one("SELECT COUNT(*) as count FROM companies WHERE year_established IS NOT NULL")
    year_cnt = year_row["count"] if year_row else 0

    evidence_row = query_one("SELECT COUNT(*) as count FROM companies WHERE evidence_url IS NOT NULL AND evidence_url != ''")
    evidence_cnt = evidence_row["count"] if evidence_row else 0

    verified_status_row = query_one("SELECT COUNT(*) as count FROM companies WHERE verification_status = 'Verified'")
    verified_cnt = verified_status_row["count"] if verified_status_row else 0

    # City quality
    city_total_row = query_one("SELECT COUNT(*) as total FROM cities")
    total_cities = city_total_row["total"] if city_total_row else 0

    rent_row = query_one("SELECT COUNT(*) as count FROM cities WHERE indicative_rent_min IS NOT NULL")
    rent_cnt = rent_row["count"] if rent_row else 0

    sal_row = query_one("SELECT COUNT(*) as count FROM cities WHERE indicative_salary_mid_lakh IS NOT NULL")
    sal_cnt = sal_row["count"] if sal_row else 0

    year_pct = round((year_cnt / total_comps * 100), 1) if total_comps > 0 else 0.0
    evidence_pct = round((evidence_cnt / total_comps * 100), 1) if total_comps > 0 else 0.0
    verif_rate = round((verified_cnt / total_comps * 100), 1) if total_comps > 0 else 0.0
    rent_pct = round((rent_cnt / total_cities * 100), 1) if total_cities > 0 else 0.0
    sal_pct = round((sal_cnt / total_cities * 100), 1) if total_cities > 0 else 0.0

    quality_metrics = DataQualityReport(
        total_records=total_comps,
        year_established_completeness_pct=year_pct,
        rent_benchmark_completeness_pct=rent_pct,
        salary_benchmark_completeness_pct=sal_pct,
        evidence_url_completeness_pct=evidence_pct,
        verification_rate_pct=verif_rate
    )

    methodology_note = (
        "GCC Atlas gathers intelligence from publicly verifiable institutional sources: official corporate newsrooms, "
        "statutory regulatory filings, state investment facilitation bodies (TS-iPASS, KITS, Invest UP, Guidance TN), "
        "and established market research reports (NASSCOM, ANAROCK, Michael Page). "
        "Source verification is an ongoing, continuous process. We deliberately display 'Data unavailable' rather than "
        "extrapolating unverified operational statistics or fabricating lease terms."
    )

    return SourcesResponse(
        total_sources=len(sources),
        sources=sources,
        quality_metrics=quality_metrics,
        methodology_note=methodology_note
    )
