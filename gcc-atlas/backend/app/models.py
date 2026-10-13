"""
Pydantic data schemas and response models for GCC Atlas
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# --- Health & Status ---
class HealthResponse(BaseModel):
    status: str
    version: str
    database_connected: bool
    total_companies: int
    total_cities: int
    ai_mode: str  # "live_llm" or "demo_mode"


# --- Companies ---
class CompanyBase(BaseModel):
    id: str
    name: str
    parent_company: Optional[str] = None
    hq_country: str
    city_id: str
    city_name: str
    sector: str
    year_established: Optional[int] = None
    business_functions: str
    short_description: str
    headcount_bracket: Optional[str] = None
    evidence_url: str
    source_id: Optional[str] = None
    source_name: str
    last_verified_date: str
    verification_status: str
    expansion_status: Optional[str] = None


class CompanyDetail(CompanyBase):
    pass


class CompanyListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[CompanyBase]
    available_cities: List[str]
    available_sectors: List[str]


# --- Cities & Comparison ---
class CityBase(BaseModel):
    id: str
    name: str
    state: str
    tier: str
    indicative_rent_min: Optional[float] = None
    indicative_rent_max: Optional[float] = None
    indicative_rent_period: Optional[str] = None
    indicative_salary_entry_lakh: Optional[float] = None
    indicative_salary_mid_lakh: Optional[float] = None
    indicative_salary_senior_lakh: Optional[float] = None
    salary_benchmark_period: Optional[str] = None
    state_incentives: Optional[str] = None
    talent_ecosystem: Optional[str] = None
    infrastructure_notes: Optional[str] = None
    tradeoff_pros: Optional[str] = None
    tradeoff_cons: Optional[str] = None
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    last_updated: Optional[str] = None
    gcc_count: int = 0


class CityListResponse(BaseModel):
    total: int
    items: List[CityBase]


class CityComparisonTradeoffSummary(BaseModel):
    summary_text: str
    cost_leader: Optional[str] = None
    talent_leader: Optional[str] = None
    infrastructure_leader: Optional[str] = None
    incentive_highlights: Dict[str, str] = {}
    data_limitations_note: str


class CityComparisonResponse(BaseModel):
    compared_cities: List[CityBase]
    tradeoff_analysis: CityComparisonTradeoffSummary


# --- Dashboard ---
class SectorDistributionItem(BaseModel):
    sector: str
    count: int
    percentage: float


class CityDistributionItem(BaseModel):
    city_name: str
    count: int
    percentage: float


class ExpansionItem(BaseModel):
    id: str
    company_name: str
    city_name: str
    announcement_title: str
    date: str
    details: str
    source_url: str
    source_name: str


class DashboardResponse(BaseModel):
    total_companies: int
    total_cities: int
    total_sectors: int
    total_sources: int
    sector_distribution: List[SectorDistributionItem]
    city_distribution: List[CityDistributionItem]
    recent_companies: List[CompanyBase]
    recent_expansions: List[ExpansionItem]
    prototype_disclaimer: str


# --- Sources & Quality ---
class SourceItem(BaseModel):
    id: str
    name: str
    url: str
    category: str
    description: Optional[str] = None
    last_checked_date: str
    reliability_tier: str
    linked_company_count: int


class DataQualityReport(BaseModel):
    total_records: int
    year_established_completeness_pct: float
    rent_benchmark_completeness_pct: float
    salary_benchmark_completeness_pct: float
    evidence_url_completeness_pct: float
    verification_rate_pct: float


class SourcesResponse(BaseModel):
    total_sources: int
    sources: List[SourceItem]
    quality_metrics: DataQualityReport
    methodology_note: str


# --- AI Research Assistant ---
class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class AssistantChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=1000)
    history: List[ChatMessage] = []


class SourceCitation(BaseModel):
    title: str
    url: str
    source_name: str
    verified_date: Optional[str] = None
    relevant_fact: str


class AssistantChatResponse(BaseModel):
    answer: str
    citations: List[SourceCitation]
    is_demo_mode: bool
    mode_badge: str
    retrieved_records_count: int
    grounding_summary: Optional[str] = None
