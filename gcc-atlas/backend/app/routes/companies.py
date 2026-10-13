"""
Companies directory API routes for GCC Atlas
Provides search, multi-filter, pagination, and detailed profiles.
"""

from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Path
from app.database import query_all, query_one
from app.models import CompanyListResponse, CompanyDetail, CompanyBase

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=CompanyListResponse)
def list_companies(
    search: Optional[str] = Query(None, description="Search keyword matching name, parent, functions, or description"),
    city: Optional[str] = Query(None, description="Filter by Indian city (e.g. Bengaluru, Hyderabad)"),
    sector: Optional[str] = Query(None, description="Filter by sector (e.g. BFSI / Fintech, Technology)"),
    verification_status: Optional[str] = Query(None, description="Filter by status (Verified, Under Verification)"),
    sort_by: str = Query("name", description="Sort field: name, year_established, city_name, last_verified_date"),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Retrieve paginated, filtered, and searchable company records."""
    where_clauses = []
    params = []

    if search and search.strip():
        term = f"%{search.strip().lower()}%"
        where_clauses.append(
            "(LOWER(name) LIKE ? OR LOWER(parent_company) LIKE ? OR LOWER(business_functions) LIKE ? OR LOWER(short_description) LIKE ?)"
        )
        params.extend([term, term, term, term])

    if city and city.strip():
        where_clauses.append("LOWER(city_name) = ?")
        params.append(city.strip().lower())

    if sector and sector.strip():
        where_clauses.append("LOWER(sector) = ?")
        params.append(sector.strip().lower())

    if verification_status and verification_status.strip():
        where_clauses.append("LOWER(verification_status) = ?")
        params.append(verification_status.strip().lower())

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # Count total
    count_sql = f"SELECT COUNT(*) as total FROM companies {where_sql}"
    total_row = query_one(count_sql, tuple(params))
    total = total_row["total"] if total_row else 0

    # Sorting safe validation
    allowed_sort_fields = {
        "name": "name",
        "year_established": "year_established",
        "city_name": "city_name",
        "last_verified_date": "last_verified_date",
        "sector": "sector"
    }
    field = allowed_sort_fields.get(sort_by, "name")
    order = "DESC" if sort_order.lower() == "desc" else "ASC"

    # Pagination
    offset = (page - 1) * limit
    list_sql = f"""
        SELECT * FROM companies
        {where_sql}
        ORDER BY {field} {order}
        LIMIT ? OFFSET ?
    """
    list_params = list(params) + [limit, offset]
    rows = query_all(list_sql, tuple(list_params))
    items = [CompanyBase(**r) for r in rows]

    total_pages = (total + limit - 1) // limit if total > 0 else 1

    # Available filter values
    cities_rows = query_all("SELECT DISTINCT city_name FROM companies ORDER BY city_name ASC")
    available_cities = [r["city_name"] for r in cities_rows]

    sectors_rows = query_all("SELECT DISTINCT sector FROM companies ORDER BY sector ASC")
    available_sectors = [r["sector"] for r in sectors_rows]

    return CompanyListResponse(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        items=items,
        available_cities=available_cities,
        available_sectors=available_sectors
    )


@router.get("/{company_id}", response_model=CompanyDetail)
def get_company_detail(company_id: str = Path(..., description="Unique company ID")):
    """Get single company profile by ID."""
    row = query_one("SELECT * FROM companies WHERE id = ?", (company_id,))
    if not row:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found.")
    return CompanyDetail(**row)
