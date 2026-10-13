-- GCC Atlas Database Schema
-- Designed for SQLite with full ANSI SQL compatibility for future PostgreSQL migration

CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    last_checked_date TEXT NOT NULL,
    reliability_tier TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    tier TEXT NOT NULL,
    indicative_rent_min REAL,
    indicative_rent_max REAL,
    indicative_rent_period TEXT,
    indicative_salary_entry_lakh REAL,
    indicative_salary_mid_lakh REAL,
    indicative_salary_senior_lakh REAL,
    salary_benchmark_period TEXT,
    state_incentives TEXT,
    talent_ecosystem TEXT,
    infrastructure_notes TEXT,
    tradeoff_pros TEXT,
    tradeoff_cons TEXT,
    source_id TEXT,
    source_url TEXT,
    last_updated TEXT,
    FOREIGN KEY (source_id) REFERENCES sources (id)
);

CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_company TEXT,
    hq_country TEXT NOT NULL,
    city_id TEXT NOT NULL,
    city_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    year_established INTEGER,
    business_functions TEXT NOT NULL,
    short_description TEXT NOT NULL,
    headcount_bracket TEXT,
    evidence_url TEXT NOT NULL,
    source_id TEXT,
    source_name TEXT NOT NULL,
    last_verified_date TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    expansion_status TEXT,
    FOREIGN KEY (city_id) REFERENCES cities (id),
    FOREIGN KEY (source_id) REFERENCES sources (id)
);

CREATE TABLE IF NOT EXISTS expansions (
    id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    city_name TEXT NOT NULL,
    announcement_title TEXT NOT NULL,
    date TEXT NOT NULL,
    details TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_name TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_companies_city ON companies(city_id);
CREATE INDEX IF NOT EXISTS idx_companies_sector ON companies(sector);
CREATE INDEX IF NOT EXISTS idx_companies_verification ON companies(verification_status);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
