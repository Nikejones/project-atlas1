# GCC Atlas — AI-Powered GCC Intelligence Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python)](https://python.org)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?style=flat&logo=sqlite)](https://sqlite.org)
[![Chart.js](https://img.shields.io/badge/Visuals-Chart.js-FF6384.svg?style=flat&logo=chartdotjs)](https://www.chartjs.org)
[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](#)

**GCC Atlas** is an enterprise-grade market intelligence platform engineered for multinational corporations, expansion strategists, commercial real estate advisors, and recruitment leaders evaluating India's **Global Capability Centre (GCC)** ecosystem.

---

## 1. Product Vision & Problem Statement

India hosts over 1,600+ Global Capability Centres employing more than 1.9 million technology, product engineering, risk modeling, and operational leaders. However, intelligence regarding:
- Which multinational corporations operate GCCs in India,
- Which metropolitan corridors (Bengaluru, Hyderabad, Pune, Gurugram, Noida, Chennai) match specific technical requirements,
- What prevailing Grade A office rental benchmarks (₹ / sq ft / month) and compensation structures (annual ₹ Lakh) look like,
- What state-level IT policies and fiscal subsidies exist,
- Where primary public evidence links reside,

is fragmented across government portals, regulatory filings, corporate press rooms, and consultancy reports.

**GCC Atlas provides a single, verifiable, searchable, and AI-assisted source of truth.**

---

## 2. Core Platform Capabilities

### 📊 Page A: GCC Intelligence Dashboard
- **Real-Time KPIs**: Dynamic metric cards computing total verified multinationals (28), metropolitan corridors (6), represented sectors (7), and institutional sources (10) directly from the database.
- **Visual Analytics**: Interactive Chart.js visualizations for **GCC Distribution by Sector** (doughnut) and **Concentration by Metro Hub** (bar chart).
- **Recent Company Additions**: Tabular summary of recently indexed corporate centers.
- **Recent Expansion Announcements**: Sourced milestones with investment figures, dates, and official corporate press room links.
- **Prototype Dataset Notice**: Transparently communicates that the MVP utilizes a curated verification sample.

### 🏢 Page B: GCC Company Directory
- **Multi-Parameter Search & Filtering**: Instant keyword search matching company names, parent corporations, and functional specializations.
- **Faceted Filters**: Dynamic dropdown filters for **City** (e.g., Bengaluru, Hyderabad, Pune, Noida, Chennai, Gurugram), **Industry Sector** (BFSI, Tech, Automotive, Healthcare, Retail, Semiconductors), and **Verification Status**.
- **Deterministic Sorting**: Sort by Company Name, Year Established, City, or Verification Date.
- **Detailed Corporate Profile Modal**: Click any company to view its headquarters country, operational scope, verified launch year, headcount bracket, business functions tag cloud, and clickable primary evidence link.
- **Honest Missing Data Handling**: Unverified attributes display as *"Data unavailable in verified source"* rather than fabricated values.

### 🗺️ Page C: GCC City Comparison
- **Interactive Multi-City Selector**: Select 2 to 4 cities simultaneously with toggle pills.
- **Side-by-Side Benchmarking Matrix**:
  - Existing GCC presence count.
  - Indicative Grade A commercial office rental ranges (`₹ / sq ft / month`).
  - Technology talent compensation benchmarks (Entry `0-2y`, Mid `3-7y`, Senior `8-12y+` in `₹ Lakh p.a.`).
  - State IT/ITeS policy incentive packages (TS-iPASS, Karnataka KITS, Invest UP, Guidance TN, Maharashtra MIDC).
  - Talent ecosystem, top universities, and engineering depth.
  - Infrastructure, international airports, road transit corridors, and metro lines.
  - Primary competitive edge vs. operational friction points.
  - Verified benchmark source links and time periods.
- **Dynamic Rule-Based Strategic Trade-Off Synthesis**: Automatically analyzes the selected cities, identifying cost leaders, talent depth champions, infrastructure highlights, and key decision trade-offs.

### 🤖 Page D: AI GCC Research Assistant
- **Retrieval-Augmented Conversational Interface**: Queries the SQLite database first to retrieve matching companies, cities, sectors, and policies before synthesizing answers.
- **Verified Source Citations**: Every response includes clickable source chips linking directly to primary publications or official websites.
- **Transparent Demo Mode**: When no external LLM API key (`GEMINI_API_KEY`) is configured or on network timeout, the backend activates a high-fidelity **rule-based local synthesizer**. The interface prominently labels this with a `DEMO MODE` badge and disclosure banner.
- **Suggested Inquiries**: One-click prompt chips for instant exploration:
  - *"Which companies in the dataset have GCCs in Noida?"*
  - *"Compare Hyderabad and Pune for a technology GCC."*
  - *"Which sectors are represented in Bengaluru?"*
  - *"What information should a company gather before setting up a GCC in India?"*

### 📚 Page E: Sources & Data Quality
- **Data Governance Scorecard**: Transparent completeness percentages across the dataset:
  - Year Established Completeness (%)
  - Office Rental Benchmark Coverage (%)
  - Tech Salary Benchmark Coverage (%)
  - Primary Evidence URL Completeness (100%)
  - Overall Verification Rate (%)
- **Institutional Sources Catalogue**: Detailed breakdown of government agencies (Invest India, TS-iPASS, Invest UP), industry associations (NASSCOM), real estate advisors (ANAROCK), salary consultants (Michael Page), and corporate newsrooms.

---

## 3. Technology Stack & Architecture

- **Backend**: Python 3.12, **FastAPI**, Pydantic v2 schemas, SQLite3 database.
- **Frontend**: Vanilla JavaScript (ES6+), semantic HTML5, custom responsive CSS design system (Inter font stack, slate/navy palette, accessible contrast).
- **Visuals**: Chart.js v4 (bundled locally in `frontend/js/chart.umd.min.js` for offline reliability).
- **API Documentation**: Interactive Swagger UI auto-generated at `/docs`.
- **Testing**: `pytest` and `FastAPI TestClient`.
- **Strict Guardrails**: No React, Node.js, or heavyweight runtime dependencies.

### Directory Structure

```text
gcc-atlas/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── assistant.py      # Conversational RAG endpoints
│   │   │   ├── cities.py         # Benchmarking & comparison logic
│   │   │   ├── companies.py      # Directory search, filter, pagination
│   │   │   ├── dashboard.py      # Dynamic KPI & distribution calculations
│   │   │   ├── health.py         # System health & database ping
│   │   │   └── sources.py        # Sources registry & completeness metrics
│   │   ├── services/
│   │   │   ├── llm_service.py    # LLM API & rule-based local synthesizer
│   │   │   └── rag_service.py    # Database retrieval & citation mapping
│   │   ├── config.py             # Settings & environment variables
│   │   ├── database.py           # SQLite connection manager & query helpers
│   │   ├── main.py               # FastAPI entry point & static file mount
│   │   └── models.py             # Pydantic request and response schemas
│   ├── data/
│   │   ├── gcc_atlas.db          # Populated SQLite database
│   │   ├── schema.sql            # Clean ANSI SQL database DDL
│   │   └── seed_data.py          # Deterministic seed script (28 MNCs, 6 cities)
│   └── tests/
│       └── test_api.py           # Automated pytest test suite
├── frontend/
│   ├── css/
│   │   └── styles.css            # Enterprise B2B SaaS design system
│   ├── js/
│   │   ├── app.js                # App navigation, global search, toast alerts
│   │   ├── assistant.js          # AI chat interface & citation cards
│   │   ├── chart.umd.min.js      # Bundled Chart.js v4 runtime
│   │   ├── cities.js             # City multi-selector & comparison matrix
│   │   ├── companies.js          # Table filters, pagination & profile modal
│   │   ├── dashboard.js          # Dashboard KPIs & Chart.js charts
│   │   └── sources.js            # Sources catalog & data quality scorecards
│   └── index.html                # Single-page application shell
├── .env.example                  # Environment configuration template
├── README.md                     # Architecture, features, and setup guide
├── requirements.txt              # Python package dependencies
└── run.py                        # One-command server startup runner
```

---

## 4. Quickstart & Installation

### Prerequisites
- Python 3.10+ (Tested on Python 3.12.4 on Windows/Linux/macOS)
- `pip`

### Step 1: Clone or Navigate to Directory
```bash
cd "C:\Users\Nikhil tyagi\.gemini\antigravity\scratch\gcc-atlas"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: (Optional) Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
*(Optional)* Add your Gemini API key if you wish to use live LLM responses:
```env
GEMINI_API_KEY="your-google-gemini-api-key"
```
> **Note**: An API key is **NOT required**. The platform includes a high-fidelity local rule-based intelligence engine that works 100% offline out-of-the-box.

### Step 4: Run the Application
```bash
python run.py
```

Open your browser to:
- **Web Application**: `http://localhost:8000`
- **FastAPI Interactive Docs**: `http://localhost:8000/docs`

---

## 5. Deployment on Vercel

GCC Atlas is fully configured for serverless deployment on **Vercel** with `@vercel/python`.

### Option A: Deploy via GitHub (Recommended)
1. Push this repository to GitHub:
   ```bash
   git remote add origin https://github.com/<your-username>/gcc-atlas.git
   git branch -M main
   git push -u origin main
   ```
2. Log into [Vercel Dashboard](https://vercel.com/) and click **Add New... > Project**.
3. Import your `gcc-atlas` repository.
4. *(Optional)* In **Environment Variables**, add `GEMINI_API_KEY` (if using live AI).
5. Click **Deploy**. Vercel will build and assign a live production URL (`https://gcc-atlas.vercel.app`).

### Option B: Deploy via Vercel CLI (Terminal)
Run from the project root:
```bash
npx vercel
```
Follow the interactive prompts:
- *Set up and deploy?* -> `Y`
- *Which scope?* -> Select your personal or team account
- *Link to existing project?* -> `N`
- *Project name?* -> `gcc-atlas`
- *Directory?* -> `./`

For production deployment:
```bash
npx vercel --prod
```

---

## 6. Running Automated Tests

Run the comprehensive test suite verifying health, dashboard KPIs, company search/filtering, city comparison, and the AI research assistant:

```bash
cd backend
pytest -v
```

All 7 test suites pass in ~1.5 seconds.

---

## 6. Sourced Seed Dataset (28 Multinational GCCs)

The database includes 28 verified multinational capability centres across 6 Indian cities:

| Company Name | Parent HQ | City | Sector | Established |
|:---|:---|:---|:---|:---:|
| **JPMorgan Chase & Co.** | United States | Bengaluru | BFSI / Fintech | 2002 |
| **Goldman Sachs India** | United States | Bengaluru | BFSI / Fintech | 2004 |
| **Microsoft IDC** | United States | Hyderabad | Technology & Software | 1998 |
| **Google India R&D** | United States | Bengaluru | Technology & Software | 2004 |
| **Amazon Development Center** | United States | Hyderabad | Technology & Software | 2004 |
| **Wells Fargo International** | United States | Hyderabad | BFSI / Fintech | 2006 |
| **Walmart Global Tech** | United States | Bengaluru | Retail & Consumer Tech | 2011 |
| **Target Enterprise Services** | United States | Bengaluru | Retail & Consumer Tech | 2005 |
| **Boeing India (BIETC)** | United States | Bengaluru | Aerospace & Defense | 2009 |
| **Airbus Digital Centre** | France | Bengaluru | Aerospace & Defense | 2007 |
| **Siemens Technology** | Germany | Bengaluru | Industrial & Automation | 2004 |
| **Mercedes-Benz (MBRDI)** | Germany | Bengaluru | Automotive & Mobility | 1996 |
| **Barclays Global Service Centre** | United Kingdom | Pune | BFSI / Fintech | 2007 |
| **Deutsche Bank Tech Centre** | Germany | Pune | BFSI / Fintech | 2006 |
| **Fidelity Investments India** | United States | Bengaluru | BFSI / Fintech | 2001 |
| **Standard Chartered GBS** | United Kingdom | Chennai | BFSI / Fintech | 2000 |
| **AstraZeneca (GITC)** | United Kingdom | Chennai | Healthcare & Pharma | 2014 |
| **PayPal India Technology Centre**| United States | Chennai | BFSI / Fintech | 2006 |
| **Intel India Development Center**| United States | Bengaluru | Semiconductors | 1998 |
| **Qualcomm India** | United States | Hyderabad | Semiconductors | 2004 |
| **Cisco Systems Globalization** | United States | Bengaluru | Technology & Software | 1995 |
| **PepsiCo GBS** | United States | Hyderabad | Retail & Consumer Tech | 2019 |
| **Novartis Corporate Center** | Switzerland | Hyderabad | Healthcare & Pharma | 2007 |
| **Bristol Myers Squibb** | United States | Hyderabad | Healthcare & Pharma | 2023 |
| **American Express GCC** | United States | Gurugram | BFSI / Fintech | 1995 |
| **Fidelity International** | United Kingdom | Gurugram | BFSI / Fintech | 2001 |
| **Samsung R&D (SRI-Noida)** | South Korea | Noida | Semiconductors | 2007 |
| **Adobe India Development Centre**| United States | Noida | Technology & Software | 1997 |

---

## 7. Known Limitations & Roadmap

1. **Dataset Scope**: The MVP intentionally limits coverage to 28 verified anchor multinational GCCs to maintain strict data veracity. Future releases will integrate verified ETL ingestion for Tier 2 hubs (Kochi, Coimbatore, Ahmedabad, Bhubaneswar, Chandigarh).
2. **Real Estate Granularity**: Micro-market rentals reflect Grade A averages (e.g., ORR in Bengaluru, HITEC City in Hyderabad). Future iterations can include building-level lease registries.
3. **Talent Supply Mapping**: Compensation figures are based on base pay benchmarks. Future integration with LinkedIn Talent Insights or EPFO payroll data will provide live attrition and hiring demand indexes.
