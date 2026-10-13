"""
City benchmarking and comparison API routes for GCC Atlas
"""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from app.database import query_all, query_one
from app.models import (
    CityListResponse,
    CityBase,
    CityComparisonResponse,
    CityComparisonTradeoffSummary
)

router = APIRouter(prefix="/cities", tags=["Cities"])


def build_tradeoff_summary(cities: List[CityBase]) -> CityComparisonTradeoffSummary:
    """
    Generate an honest, rule-based comparative synthesis highlighting
    cost differentials, talent availability, infrastructure, and state incentives.
    """
    if len(cities) < 2:
        return CityComparisonTradeoffSummary(
            summary_text="Select at least two cities to generate a side-by-side trade-off analysis.",
            data_limitations_note="A minimum of two comparative data points is required."
        )

    # 1. Cost analysis (Office rental)
    valid_rents = [c for c in cities if c.indicative_rent_min is not None]
    cost_leader = None
    if valid_rents:
        cheapest_city = min(valid_rents, key=lambda x: x.indicative_rent_min)
        priciest_city = max(valid_rents, key=lambda x: x.indicative_rent_max or x.indicative_rent_min)
        rent_diff_pct = 0
        if priciest_city.indicative_rent_min and cheapest_city.indicative_rent_min:
            rent_diff_pct = round(((priciest_city.indicative_rent_min - cheapest_city.indicative_rent_min) / priciest_city.indicative_rent_min) * 100)
        cost_leader = f"{cheapest_city.name} (~{rent_diff_pct}% lower base Grade A rent than {priciest_city.name})"

    # 2. Talent ecosystem
    valid_salaries = [c for c in cities if c.indicative_salary_mid_lakh is not None]
    talent_leader = None
    if any(c.id == "bengaluru" for c in cities):
        talent_leader = "Bengaluru (Deepest specialized engineering pool in AI & cloud architecture)"
    elif any(c.id == "hyderabad" for c in cities):
        talent_leader = "Hyderabad (Fast-scaling technical talent with deep convergence in software and pharma data science)"
    elif any(c.id == "chennai" for c in cities):
        talent_leader = "Chennai (Highest educational retention rate and engineering graduation volume)"
    elif any(c.id == "pune" for c in cities):
        talent_leader = "Pune (High retention and automotive/industrial embedded systems talent)"
    elif any(c.id == "gurugram" for c in cities):
        talent_leader = "Gurugram (Elite corporate leadership, financial risk modeling, and legal talent)"
    else:
        talent_leader = cities[0].name

    # 3. Infrastructure leader
    infra_leader = None
    if any(c.id == "hyderabad" for c in cities):
        infra_leader = "Hyderabad (8-lane Outer Ring Road, high power stability, signal-free airport connectivity)"
    elif any(c.id == "gurugram" for c in cities):
        infra_leader = "Gurugram (Proximity to Indira Gandhi International Airport T3 and DLF CyberHub)"
    elif any(c.id == "bengaluru" for c in cities):
        infra_leader = "Bengaluru (Kempegowda T2 airport, though ORR peak-hour road traffic is a friction point)"
    else:
        infra_leader = cities[0].name

    # 4. State incentives dictionary
    incentive_highlights = {}
    for c in cities:
        incentive_highlights[c.name] = c.state_incentives or "Data unavailable"

    # 5. Composite trade-off prose
    summary_parts = []
    summary_parts.append(f"Comparing **{', '.join(c.name for c in cities)}** across real estate, talent, and operational considerations:")

    if cost_leader:
        summary_parts.append(f"• **Cost Competitiveness**: {cost_leader}.")
    if talent_leader:
        summary_parts.append(f"• **Talent Breadth**: {talent_leader}.")
    if infra_leader:
        summary_parts.append(f"• **Commute & Municipal Infrastructure**: {infra_leader}.")

    # Highlight trade-offs
    tradeoff_notes = []
    for c in cities:
        pros = c.tradeoff_pros or "Data unavailable"
        cons = c.tradeoff_cons or "Data unavailable"
        tradeoff_notes.append(f"**{c.name}**: Advantage: {pros} | Limitation: {cons}")
    summary_parts.append("\n**Key Decision Trade-offs**:\n" + "\n".join(tradeoff_notes))

    data_limitations_note = (
        "Methodology Disclosure: Benchmarks are compiled from ANAROCK Commercial Real Estate (H1 2024) and "
        "Michael Page Tech Salary Survey (2023-2024). Rental numbers reflect prevailing Grade A IT park micro-market asking rates. "
        "Compensation numbers reflect base salary bands and exclude long-term equity incentives (RSUs/ESOPs). "
        "City suitability is an analytical decision aid, not a deterministic ranking."
    )

    return CityComparisonTradeoffSummary(
        summary_text="\n\n".join(summary_parts),
        cost_leader=cost_leader,
        talent_leader=talent_leader,
        infrastructure_leader=infra_leader,
        incentive_highlights=incentive_highlights,
        data_limitations_note=data_limitations_note
    )


@router.get("", response_model=CityListResponse)
def list_cities():
    """Retrieve all benchmark cities with their associated GCC counts."""
    rows = query_all("""
        SELECT c.*, COUNT(comp.id) as gcc_count
        FROM cities c
        LEFT JOIN companies comp ON c.id = comp.city_id
        GROUP BY c.id
        ORDER BY gcc_count DESC, c.name ASC
    """)
    items = [CityBase(**r) for r in rows]
    return CityListResponse(total=len(items), items=items)


@router.get("/compare", response_model=CityComparisonResponse)
def compare_cities(
    city_ids: str = Query(..., description="Comma-separated city IDs to compare (e.g. bengaluru,hyderabad,pune)")
):
    """Compare 2 to 4 cities side-by-side with dynamic trade-off analysis."""
    ids = [cid.strip().lower() for cid in city_ids.split(",") if cid.strip()]
    if len(ids) < 2:
        raise HTTPException(status_code=400, detail="Please select at least 2 cities for side-by-side comparison.")
    if len(ids) > 4:
        raise HTTPException(status_code=400, detail="Comparison is limited to a maximum of 4 cities simultaneously.")

    placeholders = ",".join("?" for _ in ids)
    sql = f"""
        SELECT c.*, COUNT(comp.id) as gcc_count
        FROM cities c
        LEFT JOIN companies comp ON c.id = comp.city_id
        WHERE c.id IN ({placeholders})
        GROUP BY c.id
    """
    rows = query_all(sql, tuple(ids))
    if not rows:
        raise HTTPException(status_code=404, detail="None of the specified cities were found in the database.")

    # Order in the same sequence as requested
    city_map = {r["id"]: CityBase(**r) for r in rows}
    ordered_cities = [city_map[cid] for cid in ids if cid in city_map]

    tradeoff_analysis = build_tradeoff_summary(ordered_cities)

    return CityComparisonResponse(
        compared_cities=ordered_cities,
        tradeoff_analysis=tradeoff_analysis
    )
