"""
RAG Service for GCC Atlas
Retrieves relevant company records, city benchmarks, state policies, and sources from SQLite.
"""

import re
from typing import Dict, Any, List, Tuple
from app.database import query_all, query_one
from app.models import SourceCitation


def extract_keywords(text: str) -> List[str]:
    """Extract normalized lowercase tokens from search text."""
    words = re.findall(r'[a-zA-Z0-9\+\#]+', text.lower())
    stop_words = {"the", "a", "an", "in", "on", "of", "and", "or", "for", "with", "at", "by", "from", "to", "is", "are", "what", "which", "how", "who", "where", "can", "should", "does", "have", "has", "do"}
    return [w for w in words if w not in stop_words and len(w) > 1]


def retrieve_context(user_query: str) -> Dict[str, Any]:
    """
    Search local database for companies, cities, sectors, and expansion data
    relevant to the user's research query.
    """
    query_lower = user_query.lower()
    citations: List[SourceCitation] = []
    retrieved_companies = []
    retrieved_cities = []
    retrieved_expansions = []

    # 1. City Matching
    city_aliases = {
        "bengaluru": ["bengaluru", "bangalore"],
        "hyderabad": ["hyderabad", "cyberabad"],
        "pune": ["pune"],
        "gurugram": ["gurugram", "gurgaon"],
        "noida": ["noida", "greater noida"],
        "chennai": ["chennai", "madras"]
    }

    matched_city_ids = set()
    for city_id, aliases in city_aliases.items():
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', query_lower):
                matched_city_ids.add(city_id)
                break

    # 2. Sector Matching
    sector_keywords = {
        "BFSI / Fintech": ["bfsi", "bank", "banking", "finance", "fintech", "financial", "trading", "investment", "payments"],
        "Technology & Software": ["tech", "technology", "software", "cloud", "saas", "ai", "platform", "it"],
        "Healthcare & Pharma": ["pharma", "pharmaceutical", "health", "healthcare", "biotech", "clinical", "drug"],
        "Automotive & Mobility": ["auto", "automotive", "mobility", "vehicle", "car", "autonomous"],
        "Aerospace & Defense": ["aerospace", "aviation", "defense", "aircraft", "flight"],
        "Retail & Consumer Tech": ["retail", "consumer", "ecommerce", "merchandise", "supply chain"],
        "Semiconductors & Electronics": ["semiconductor", "chip", "silicon", "hardware", "electronics"]
    }

    matched_sectors = set()
    for sector_name, kws in sector_keywords.items():
        for kw in kws:
            if re.search(r'\b' + re.escape(kw) + r'\b', query_lower):
                matched_sectors.add(sector_name)
                break

    # 3. Retrieve Cities if matched
    if matched_city_ids:
        placeholders = ",".join("?" for _ in matched_city_ids)
        cities_rows = query_all(f"SELECT * FROM cities WHERE id IN ({placeholders})", tuple(matched_city_ids))
        for row in cities_rows:
            retrieved_cities.append(row)
            if row.get("source_url"):
                citations.append(SourceCitation(
                    title=f"{row['name']} Real Estate & Talent Benchmark",
                    url=row["source_url"],
                    source_name="Official State / Industry Real Estate Benchmark",
                    verified_date=row.get("last_updated"),
                    relevant_fact=f"Rent: ₹{row.get('indicative_rent_min')}-₹{row.get('indicative_rent_max')}/sq ft/mo. Mid-salary: ₹{row.get('indicative_salary_mid_lakh')}L."
                ))

    # 4. Search Companies by City, Sector, or Keyword
    company_sql_conditions = []
    company_params = []

    if matched_city_ids:
        placeholders = ",".join("?" for _ in matched_city_ids)
        company_sql_conditions.append(f"city_id IN ({placeholders})")
        company_params.extend(list(matched_city_ids))

    if matched_sectors:
        placeholders = ",".join("?" for _ in matched_sectors)
        company_sql_conditions.append(f"sector IN ({placeholders})")
        company_params.extend(list(matched_sectors))

    # Also search by company name tokens
    tokens = extract_keywords(user_query)
    token_clauses = []
    token_params = []
    for token in tokens:
        if len(token) >= 3:
            token_clauses.append("(LOWER(name) LIKE ? OR LOWER(business_functions) LIKE ?)")
            token_params.extend([f"%{token}%", f"%{token}%"])

    if token_clauses:
        # Check if any company matches name directly
        direct_name_match = query_all(
            f"SELECT * FROM companies WHERE {' OR '.join(token_clauses)}",
            tuple(token_params)
        )
        for row in direct_name_match:
            if row not in retrieved_companies:
                retrieved_companies.append(row)

    if company_sql_conditions:
        sql = f"SELECT * FROM companies WHERE {' AND '.join(company_sql_conditions)} LIMIT 15"
        filtered_comps = query_all(sql, tuple(company_params))
        for comp in filtered_comps:
            if comp not in retrieved_companies:
                retrieved_companies.append(comp)

    # If nothing matched yet and query is general, pull top relevant or general records
    is_setup_guidance = any(k in query_lower for k in ["gather", "set up", "setup", "establishing", "starting", "checklist", "information should", "step", "entry"])
    if is_setup_guidance:
        # Load all cities summary for comprehensive benchmark context
        all_cities = query_all("SELECT id, name, state, indicative_rent_min, indicative_rent_max, indicative_salary_mid_lakh, state_incentives, tradeoff_pros FROM cities")
        retrieved_cities = all_cities
        # Add Invest India & NASSCOM citations
        citations.append(SourceCitation(
            title="Invest India - GCC Strategic Transformation Framework",
            url="https://www.investindia.gov.in/team-india-blogs/global-capability-centres-indias-strategic-transformation",
            source_name="Invest India (Govt of India)",
            verified_date="2024-09-20",
            relevant_fact="National regulatory, tax, and site evaluation advisory for multinational capability centers."
        ))
        citations.append(SourceCitation(
            title="NASSCOM - Zinnov India GCC Landscape Report",
            url="https://nasscom.in/knowledge-center/publications/india-gcc-landscape-report-2024",
            source_name="NASSCOM",
            verified_date="2024-08-15",
            relevant_fact="Benchmark operational maturity, headcount scaling, and talent availability."
        ))

    # Add citations for retrieved companies
    for comp in retrieved_companies[:6]:
        if comp.get("evidence_url"):
            citations.append(SourceCitation(
                title=f"{comp['name']} ({comp['city_name']}) GCC Record",
                url=comp["evidence_url"],
                source_name=comp.get("source_name", "Verified Sourced Entity"),
                verified_date=comp.get("last_verified_date"),
                relevant_fact=f"Sector: {comp['sector']} | Established: {comp.get('year_established') or 'Data unavailable'} | Core Functions: {comp['business_functions']}"
            ))

    # Deduplicate citations by URL
    seen_urls = set()
    unique_citations = []
    for c in citations:
        if c.url not in seen_urls:
            seen_urls.add(c.url)
            unique_citations.append(c)

    return {
        "matched_city_ids": list(matched_city_ids),
        "matched_sectors": list(matched_sectors),
        "retrieved_companies": retrieved_companies,
        "retrieved_cities": retrieved_cities,
        "retrieved_expansions": retrieved_expansions,
        "citations": unique_citations,
        "is_setup_guidance": is_setup_guidance
    }
