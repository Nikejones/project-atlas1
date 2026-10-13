"""
GCC Atlas Seed Script
Populates SQLite database with 28 verified multinational company GCC records,
6 Indian metro city benchmarks, 10 primary & secondary sources, and recent expansions.
"""

import sqlite3
import os
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "gcc_atlas.db"
SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"

SOURCES = [
    {
        "id": "invest-india",
        "name": "Invest India - National Investment Promotion & Facilitation Agency",
        "url": "https://www.investindia.gov.in/team-india-blogs/global-capability-centres-indias-strategic-transformation",
        "category": "Government Agency",
        "description": "Official national investment promotion body under the Ministry of Commerce and Industry.",
        "last_checked_date": "2024-09-20",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "nasscom-gcc-report",
        "name": "NASSCOM - Zinnov India GCC Landscape Report",
        "url": "https://nasscom.in/knowledge-center/publications/india-gcc-landscape-report-2024",
        "category": "Industry Association",
        "description": "Apex industry trade association tracking over 1,600+ Global Capability Centres in India.",
        "last_checked_date": "2024-08-15",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "anarock-commercial",
        "name": "ANAROCK Commercial Real Estate Research",
        "url": "https://www.anarock.com/research-insights",
        "category": "Consultancy Report",
        "description": "Leading Indian real estate consultancy tracking Grade A office micro-market lease rentals.",
        "last_checked_date": "2024-07-30",
        "reliability_tier": "Verified Secondary"
    },
    {
        "id": "michael-page-salary",
        "name": "Michael Page India Salary & Employment Outlook",
        "url": "https://www.michaelpage.co.in/salary-guide",
        "category": "Consultancy Report",
        "description": "Annual compensation benchmark covering technology, BFSI, and executive hiring across India.",
        "last_checked_date": "2024-06-10",
        "reliability_tier": "Verified Secondary"
    },
    {
        "id": "telangana-it-dept",
        "name": "ITE&C Department, Government of Telangana",
        "url": "https://it.telangana.gov.in",
        "category": "Government Agency",
        "description": "Official Department of Information Technology, Electronics & Communications, Telangana.",
        "last_checked_date": "2024-09-01",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "karnataka-kits",
        "name": "Karnataka Innovation & Technology Society (KITS)",
        "url": "https://kits.karnataka.gov.in",
        "category": "Government Agency",
        "description": "Official Department of Electronics, IT, Bt and S&T, Government of Karnataka.",
        "last_checked_date": "2024-09-05",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "invest-up",
        "name": "Invest UP - Government of Uttar Pradesh",
        "url": "https://investup.org.in",
        "category": "Government Agency",
        "description": "Investment promotion and facilitation agency of the Government of Uttar Pradesh.",
        "last_checked_date": "2024-08-22",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "guidance-tamilnadu",
        "name": "Guidance Tamil Nadu - Investment Promotion Agency",
        "url": "https://investingintamilnadu.com",
        "category": "Government Agency",
        "description": "Government of Tamil Nadu nodal agency for investment promotion and single window facilitation.",
        "last_checked_date": "2024-08-18",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "company-newsrooms",
        "name": "Global MNC Corporate Newsrooms & Investor Relations",
        "url": "https://www.sec.gov/edgar",
        "category": "Company Newsroom",
        "description": "Direct official announcements, 10-K regulatory disclosures, and press releases issued by multinational parents.",
        "last_checked_date": "2024-09-28",
        "reliability_tier": "Primary Official"
    },
    {
        "id": "economic-times",
        "name": "The Economic Times - Technology & GCC Desk",
        "url": "https://economictimes.indiatimes.com/tech",
        "category": "Financial Press",
        "description": "Leading Indian business daily tracking corporate GCC expansions, leases, and leadership appointments.",
        "last_checked_date": "2024-10-01",
        "reliability_tier": "Verified Secondary"
    }
]

CITIES = [
    {
        "id": "bengaluru",
        "name": "Bengaluru",
        "state": "Karnataka",
        "tier": "Tier 1 Mega Hub",
        "indicative_rent_min": 75.0,
        "indicative_rent_max": 125.0,
        "indicative_rent_period": "H1 2024 (Grade A Outer Ring Road & Whitefield)",
        "indicative_salary_entry_lakh": 8.0,
        "indicative_salary_mid_lakh": 22.0,
        "indicative_salary_senior_lakh": 45.0,
        "salary_benchmark_period": "2023-2024 Tech GCC Survey",
        "state_incentives": "Karnataka IT Policy 2020-25 provides 100% stamp duty exemption on lease/sale agreements, patent cost reimbursement up to ₹10 Lakh, and anchor unit capital subsidies outside Zone 3. Power tariff concession of ₹1/unit for 3 years.",
        "talent_ecosystem": "India's highest concentration of specialized engineering talent (est. 450,000+ tech professionals in GCCs). Premier institutes include IISc, IIIT Bangalore, RVCE, BMSCE. Unmatched depth in Generative AI, cloud infrastructure, and silicon design.",
        "infrastructure_notes": "Kempegowda International Airport (T2 opened 2023). Namma Metro Phase 2 connecting Outer Ring Road and airport corridor under active execution. Road traffic congestion along Silk Board and Marathahalli remains the primary operational friction.",
        "tradeoff_pros": "Unmatched senior engineering talent depth; highest concentration of tech venture capital & product leadership; mature supplier and vendor ecosystem.",
        "tradeoff_cons": "Highest Grade A office rentals among Tier 1 hubs; acute peak-hour traffic bottlenecks along Outer Ring Road; intense competition for talent causing 16-20% attrition.",
        "source_id": "anarock-commercial",
        "source_url": "https://www.anarock.com/research-insights",
        "last_updated": "2024-09-15"
    },
    {
        "id": "hyderabad",
        "name": "Hyderabad",
        "state": "Telangana",
        "tier": "Tier 1 Mega Hub",
        "indicative_rent_min": 58.0,
        "indicative_rent_max": 88.0,
        "indicative_rent_period": "H1 2024 (HITEC City, Financial District, Knowledge City)",
        "indicative_salary_entry_lakh": 6.8,
        "indicative_salary_mid_lakh": 18.5,
        "indicative_salary_senior_lakh": 38.0,
        "salary_benchmark_period": "2023-2024 Tech GCC Survey",
        "state_incentives": "Telangana ICT Policy 2.0 & GCC Framework. TS-iPASS single-window statutory clearance within 15 days. 100% stamp duty reimbursement on first lease/purchase. Power tariff subsidy of ₹1.5/unit for 5 years. Tailored incentives for mega projects (>₹500 Cr or >1,000 jobs).",
        "talent_ecosystem": "Rapidly expanding talent hub anchored by IIIT Hyderabad, IIT Hyderabad, BITS Pilani Hyderabad, and Osmania University. Strong cross-domain convergence between cloud software and life sciences / pharmaceutical data science.",
        "infrastructure_notes": "Rajiv Gandhi International Airport connected via a signal-free 8-lane Outer Ring Road (158 km ring). Operational Hyderabad Metro Red and Blue lines. Continuous 24/7 industrial power reliability and planned Financial District skyscraper clusters.",
        "tradeoff_pros": "Superior municipal road infrastructure and rapid airport commute; aggressive state government single-window facilitation; 20-30% lower real estate costs than Bengaluru.",
        "tradeoff_cons": "Talent pool size is roughly 60% of Bengaluru; emerging talent bidding wars in AI and specialized risk modeling as more mega GCCs enter concurrently.",
        "source_id": "telangana-it-dept",
        "source_url": "https://it.telangana.gov.in",
        "last_updated": "2024-09-18"
    },
    {
        "id": "pune",
        "name": "Pune",
        "state": "Maharashtra",
        "tier": "Tier 1 Established",
        "indicative_rent_min": 52.0,
        "indicative_rent_max": 78.0,
        "indicative_rent_period": "H1 2024 (Hinjawadi, Kharadi, Magarpatta)",
        "indicative_salary_entry_lakh": 5.8,
        "indicative_salary_mid_lakh": 16.0,
        "indicative_salary_senior_lakh": 34.0,
        "salary_benchmark_period": "2023-2024 Tech GCC Survey",
        "state_incentives": "Maharashtra IT/ITeS Policy offers 100% electricity duty exemption for 10-15 years, stamp duty exemptions for IT park leases, and additional floor space index (FSI) up to 200% over base limits. Subsidies on green building certifications.",
        "talent_ecosystem": "'Oxford of the East' with 110+ engineering institutions including COEP Technological University, Pune University, Symbiosis, and MIT World Peace. Renowned for automotive embedded software, manufacturing digital twins, and investment banking operations.",
        "infrastructure_notes": "Pune International Airport (new terminal operational 2024; limited international direct flights). Pune Metro Line 1 & Line 2 expanding. Direct 3-hour expressway access to Mumbai commercial capital and JNPT seaport.",
        "tradeoff_pros": "High talent stickiness and lower attrition (12-14%); proximity to Mumbai financial headquarters; established automotive and industrial digital capabilities.",
        "tradeoff_cons": "Limited direct international flight routes (frequent transit via Mumbai or Delhi); peak-hour traffic bottlenecks on Hinjawadi Phase 1-3 access roads.",
        "source_id": "anarock-commercial",
        "source_url": "https://www.anarock.com/research-insights",
        "last_updated": "2024-09-10"
    },
    {
        "id": "gurugram",
        "name": "Gurugram",
        "state": "Haryana",
        "tier": "Tier 1 Established (NCR)",
        "indicative_rent_min": 72.0,
        "indicative_rent_max": 118.0,
        "indicative_rent_period": "H1 2024 (DLF Cyber City, Golf Course Road)",
        "indicative_salary_entry_lakh": 7.2,
        "indicative_salary_mid_lakh": 20.0,
        "indicative_salary_senior_lakh": 42.0,
        "salary_benchmark_period": "2023-2024 Tech GCC Survey",
        "state_incentives": "Haryana Enterprises & Employment Policy (HEEP). Net SGST reimbursement up to 50% for 7 years for anchor units. Employment generation subsidy of ₹48,000 per local employee per annum for 7 years. Stamp duty refund up to 75%.",
        "talent_ecosystem": "Access to the combined National Capital Region (NCR) talent pool. Supported by IIT Delhi, Delhi Technological University (DTU), NSUT, IIIT Delhi, and IIM Rohtak. Exceptional concentration of senior management, legal counsel, and financial risk analysts.",
        "infrastructure_notes": "Direct 15-20 minute expressway proximity to Indira Gandhi International Airport (DEL Terminal 3). Operational Delhi Metro Yellow Line and Rapid Metro Gurugram. High concentration of Fortune 500 corporate headquarters.",
        "tradeoff_pros": "Immediate proximity to international aviation hub and central government ministries; top-tier corporate real estate developments (CyberHub, One Horizon); elite leadership talent.",
        "tradeoff_cons": "High operational real estate costs comparable to Bengaluru; seasonal severe air quality challenges (AQI) in winter months; municipal water and civic infrastructure disparities outside private IT parks.",
        "source_id": "anarock-commercial",
        "source_url": "https://www.anarock.com/research-insights",
        "last_updated": "2024-09-12"
    },
    {
        "id": "noida",
        "name": "Noida",
        "state": "Uttar Pradesh",
        "tier": "Tier 1 Established (NCR)",
        "indicative_rent_min": 44.0,
        "indicative_rent_max": 68.0,
        "indicative_rent_period": "H1 2024 (Noida-Greater Noida Expressway, Sector 62/125)",
        "indicative_salary_entry_lakh": 5.2,
        "indicative_salary_mid_lakh": 14.5,
        "indicative_salary_senior_lakh": 31.0,
        "salary_benchmark_period": "2023-2024 Tech GCC Survey",
        "state_incentives": "Uttar Pradesh IT & Electronics Policy. Capital investment subsidy up to 25% of fixed capital investment. 100% stamp duty exemption. 100% electricity duty exemption for 10 years. Special land allotment concessions along expressway IT corridors.",
        "talent_ecosystem": "Dense cluster of technical universities including Dr. A.P.J. Abdul Kalam Technical University (AKTU) network, Shiv Nadar University, Amity University, and Gautam Buddha University. Major center for consumer electronics firmware and mobile software.",
        "infrastructure_notes": "Multi-lane Noida-Greater Noida Expressway and DND Flyway. Operational Delhi Metro Blue Line and Noida Aqua Metro. Upcoming Noida International Airport at Jewar (Phase 1 scheduled 2025) provides long-term logistics and passenger upside.",
        "tradeoff_pros": "Significantly lower commercial occupancy costs (30-40% cheaper than Gurugram); modern wide-grid urban road layout; aggressive UP state capital subsidy framework.",
        "tradeoff_cons": "Perception lag regarding lifestyle amenities compared to South Delhi or Gurugram; fewer ultra-senior executive engineering leaders requiring recruitment from other hubs.",
        "source_id": "invest-up",
        "source_url": "https://investup.org.in",
        "last_updated": "2024-09-14"
    },
    {
        "id": "chennai",
        "name": "Chennai",
        "state": "Tamil Nadu",
        "tier": "Tier 1 Established",
        "indicative_rent_min": 54.0,
        "indicative_rent_max": 80.0,
        "indicative_rent_period": "H1 2024 (OMR IT Expressway, Guindy, Porur)",
        "indicative_salary_entry_lakh": 6.0,
        "indicative_salary_mid_lakh": 16.8,
        "indicative_salary_senior_lakh": 35.5,
        "salary_benchmark_period": "2023-2024 Tech GCC Survey",
        "state_incentives": "Tamil Nadu IT Policy 2023 & R&D Policy. Anchor unit capital subsidies up to 25%, 100% stamp duty exemption, electricity tax exemption for 5 years, and EPF contribution reimbursement up to ₹24,000 per employee per year for women employees.",
        "talent_ecosystem": "India's highest college gross enrollment ratio; anchors Anna University, IIT Madras (IITM Research Park), and premier engineering institutions. Nation's SaaS capital with unmatched talent retention rates (sub-12% attrition).",
        "infrastructure_notes": "Chennai International Airport (MAA). Chennai Metro Phase 2 under active tunneling along Old Mahabalipuram Road (OMR IT corridor). 3 major deep-water seaports and primary undersea telecom cable landing station providing ultra-low international latency.",
        "tradeoff_pros": "Lowest voluntary employee attrition rates among major tech hubs; deep capabilities in fintech, automotive software, and biomedical analytics; strong hardware and data infrastructure.",
        "tradeoff_cons": "Ongoing Chennai Metro Phase 2 construction causes traffic detours on OMR; tropical climate with high summer humidity; perception among some North Indian talent as culturally less cosmopolitan.",
        "source_id": "guidance-tamilnadu",
        "source_url": "https://investingintamilnadu.com",
        "last_updated": "2024-09-16"
    }
]

COMPANIES = [
    {
        "id": "jpmorgan-chase",
        "name": "JPMorgan Chase & Co.",
        "parent_company": "JPMorgan Chase & Co.",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "BFSI / Fintech",
        "year_established": 2002,
        "business_functions": "Algorithmic Trading Systems, Quantitative Risk Modeling, Cloud Core Banking, Cybersecurity & Identity Protection",
        "short_description": "Operates critical global technology and operational infrastructure managing over $3 trillion in daily payments across global markets.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.jpmorganchase.com/about/our-business/global-technology",
        "source_id": "company-newsrooms",
        "source_name": "JPMorgan Chase Global Technology Portal",
        "last_verified_date": "2024-09-12",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "goldman-sachs",
        "name": "Goldman Sachs India",
        "parent_company": "The Goldman Sachs Group, Inc.",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "BFSI / Fintech",
        "year_established": 2004,
        "business_functions": "Electronic Trading Architecture, Distributed Ledger Technologies, Quantitative Investment Research, Global Risk Compliance",
        "short_description": "Bengaluru campus is Goldman Sachs' second largest global engineering location after New York, driving core Wall Street platforms.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.goldmansachs.com/our-firm/locations/bengaluru.html",
        "source_id": "company-newsrooms",
        "source_name": "Goldman Sachs Global Locations Directory",
        "last_verified_date": "2024-09-10",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "microsoft-idc",
        "name": "Microsoft India Development Center (IDC)",
        "parent_company": "Microsoft Corporation",
        "hq_country": "United States",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "Technology & Software",
        "year_established": 1998,
        "business_functions": "Azure Hyper-Scale Cloud, Generative AI Platforms (Copilot), Microsoft 365 Core Services, Windows Kernel Engineering",
        "short_description": "Microsoft's premier R&D facility outside Redmond, Washington; plays a pivotal role in engineering core cloud and foundation AI systems.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.microsoft.com/en-in/msidc",
        "source_id": "company-newsrooms",
        "source_name": "Microsoft IDC Official Portal",
        "last_verified_date": "2024-09-15",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "google-india-rd",
        "name": "Google India R&D",
        "parent_company": "Alphabet Inc.",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Technology & Software",
        "year_established": 2004,
        "business_functions": "Search Ranking Algorithms, Google Cloud Infrastructure, Android Mobile Operating System, Multilingual Speech AI",
        "short_description": "Pioneered key technologies for Google Maps, Search, and Cloud with major innovation centers in Bengaluru and Hyderabad.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://about.google/locations/?region=asia-pacific",
        "source_id": "company-newsrooms",
        "source_name": "Google Global Locations & About Portal",
        "last_verified_date": "2024-09-14",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "amazon-dev-center",
        "name": "Amazon Development Center India",
        "parent_company": "Amazon.com, Inc.",
        "hq_country": "United States",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "Technology & Software",
        "year_established": 2004,
        "business_functions": "AWS Distributed Compute & Storage, Alexa Natural Language Processing, Global Fulfillment Optimization, Retail Payments",
        "short_description": "Hosts Amazon's single largest company-owned campus in the world (9.5-acre campus in Hyderabad) housing thousands of AWS engineers.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.aboutamazon.in/news/workplace/amazons-largest-campus-in-the-world",
        "source_id": "company-newsrooms",
        "source_name": "Amazon Day One India Newsroom",
        "last_verified_date": "2024-09-18",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "wells-fargo-india",
        "name": "Wells Fargo International Solutions",
        "parent_company": "Wells Fargo & Company",
        "hq_country": "United States",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "BFSI / Fintech",
        "year_established": 2006,
        "business_functions": "Consumer Lending Platforms, Real-Time Fraud Surveillance, Commercial Banking APIs, Enterprise Data Architecture",
        "short_description": "Major strategic delivery and innovation center supporting consumer banking, risk analytics, and enterprise technology.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.wellsfargo.com/about/corporate/international/india/",
        "source_id": "company-newsrooms",
        "source_name": "Wells Fargo India Corporate Gateway",
        "last_verified_date": "2024-08-25",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "walmart-global-tech",
        "name": "Walmart Global Tech India",
        "parent_company": "Walmart Inc.",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Retail & Consumer Tech",
        "year_established": 2011,
        "business_functions": "Omnichannel Inventory Optimization, Computer Vision for Checkout, Supply Chain Digital Twins, Cloud POS Architecture",
        "short_description": "Powers digital and store capabilities for over 240 million weekly customer transactions across Walmart's global retail network.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://tech.walmart.com/content/walmart-global-tech/en_in.html",
        "source_id": "company-newsrooms",
        "source_name": "Walmart Global Tech Official Portal",
        "last_verified_date": "2024-09-02",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "target-tech",
        "name": "Target Enterprise Services India",
        "parent_company": "Target Corporation",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Retail & Consumer Tech",
        "year_established": 2005,
        "business_functions": "Digital Guest Experience, Predictive Merchandising AI, Robotic Warehouse Automation Software, Supply Chain Analytics",
        "short_description": "Fully integrated capability center driving retail technology, 3D digital product design, and supply chain modeling for Target US.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://corporate.target.com/careers/india",
        "source_id": "company-newsrooms",
        "source_name": "Target Corporate Careers & India Hub",
        "last_verified_date": "2024-08-28",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "boeing-bietc",
        "name": "Boeing India Engineering & Technology Center (BIETC)",
        "parent_company": "The Boeing Company",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Aerospace & Defense",
        "year_established": 2009,
        "business_functions": "Avionics Software Engineering, Aerodynamics Modeling & CFD, Digital Aviation Analytics, Flight Deck Management Systems",
        "short_description": "Boeing's largest engineering investment outside the United States, operating a state-of-the-art 43-acre campus at Aerospace Park.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.boeing.co.in/boeing-in-india/engineering-and-technology.page",
        "source_id": "company-newsrooms",
        "source_name": "Boeing India Engineering Overview",
        "last_verified_date": "2024-09-16",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "airbus-digital-centre",
        "name": "Airbus India Digital Centre",
        "parent_company": "Airbus SE",
        "hq_country": "France",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Aerospace & Defense",
        "year_established": 2007,
        "business_functions": "In-Flight Analytics, Cybersecurity for Flight Operations, Aircraft Digital Twin Engineering, Smart Factory Solutions",
        "short_description": "Drives end-to-end digital transformation for commercial aircraft, defense systems, and space applications across Airbus programs.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://www.airbus.com/en/our-worldwide-presence/airbus-in-asia/airbus-in-india",
        "source_id": "company-newsrooms",
        "source_name": "Airbus Worldwide Presence - India",
        "last_verified_date": "2024-08-19",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "siemens-technology",
        "name": "Siemens Technology and Services",
        "parent_company": "Siemens AG",
        "hq_country": "Germany",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Industrial & Automation",
        "year_established": 2004,
        "business_functions": "Industrial IoT (MindSphere), Factory Automation Firmware, Smart Grid Energy Management, Generative AI for Manufacturing",
        "short_description": "Flagship global research and software development center delivering industrial automation and smart infrastructure innovations.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.siemens.com/in/en/company/about/siemens-in-india.html",
        "source_id": "company-newsrooms",
        "source_name": "Siemens AG India Corporate Portal",
        "last_verified_date": "2024-09-08",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "mercedes-benz-mbrdi",
        "name": "Mercedes-Benz R&D India (MBRDI)",
        "parent_company": "Mercedes-Benz Group AG",
        "hq_country": "Germany",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Automotive & Mobility",
        "year_established": 1996,
        "business_functions": "Autonomous Driving Software (Level 2+/Level 3), Battery Management Telematics, MB.OS Infotainment, Crash Simulation CAE",
        "short_description": "Largest R&D facility for Mercedes-Benz Group outside of Stuttgart, Germany; plays a leading role in vehicle software architecture.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.mbrdi.co.in/",
        "source_id": "company-newsrooms",
        "source_name": "MBRDI Official Corporate Site",
        "last_verified_date": "2024-09-11",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "barclays-gsc",
        "name": "Barclays Global Service Centre",
        "parent_company": "Barclays PLC",
        "hq_country": "United Kingdom",
        "city_id": "pune",
        "city_name": "Pune",
        "sector": "BFSI / Fintech",
        "year_established": 2007,
        "business_functions": "Real-Time Payment Rail Modernization, Cyber Security Operations, Fraud Analytics Machine Learning, Global Corporate Banking",
        "short_description": "Major technology and operations hub situated in Hinjawadi and Kharadi, delivering high-availability resilience for Barclays global retail & investment bank.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://home.barclays/careers/our-locations/india/",
        "source_id": "company-newsrooms",
        "source_name": "Barclays Global Careers - India",
        "last_verified_date": "2024-09-04",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "deutsche-bank-tech",
        "name": "Deutsche Bank Tech Centre",
        "parent_company": "Deutsche Bank AG",
        "hq_country": "Germany",
        "city_id": "pune",
        "city_name": "Pune",
        "sector": "BFSI / Fintech",
        "year_established": 2006,
        "business_functions": "Investment Bank Trading Platforms, Anti-Money Laundering Surveillance, Cloud Transformation, Liquidity Risk Reporting",
        "short_description": "Core software engineering and digital transformation arm powering Deutsche Bank's Corporate Bank and Investment Bank globally.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.db.com/india/company/technology.htm",
        "source_id": "company-newsrooms",
        "source_name": "Deutsche Bank India Corporate Portal",
        "last_verified_date": "2024-08-30",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "fidelity-investments",
        "name": "Fidelity Investments India",
        "parent_company": "FMR LLC",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "BFSI / Fintech",
        "year_established": 2001,
        "business_functions": "Asset Management Technology, 401(k) Retirement Platforms, Brokerage Clearing Infrastructure, Cloud Modernization",
        "short_description": "Delivers core technology solutions, data architecture, and operations for Fidelity's institutional and personal investing businesses.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://india.fidelity.com/",
        "source_id": "company-newsrooms",
        "source_name": "Fidelity Investments India Portal",
        "last_verified_date": "2024-09-14",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "standard-chartered-gbs",
        "name": "Standard Chartered Global Business Services",
        "parent_company": "Standard Chartered PLC",
        "hq_country": "United Kingdom",
        "city_id": "chennai",
        "city_name": "Chennai",
        "sector": "BFSI / Fintech",
        "year_established": 2000,
        "business_functions": "Cross-Border Trade Finance Systems, Financial Crime Compliance AI, Global Clearing Platforms, Wealth Management APIs",
        "short_description": "Standard Chartered's flagship global capabilities center in Chennai (DLF Cybercity & Haddows Road), employing over 20,000 professionals across India.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.sc.com/en/about/our-locations/india/",
        "source_id": "company-newsrooms",
        "source_name": "Standard Chartered Global Operations Hub",
        "last_verified_date": "2024-09-06",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "astrazeneca-gitc",
        "name": "AstraZeneca Global Innovation & Technology Centre",
        "parent_company": "AstraZeneca PLC",
        "hq_country": "United Kingdom",
        "city_id": "chennai",
        "city_name": "Chennai",
        "sector": "Healthcare & Pharma",
        "year_established": 2014,
        "business_functions": "Clinical Trial Informatics, Pharmacovigilance & Drug Safety AI, Supply Chain Serialization, Commercial Operations Analytics",
        "short_description": "AstraZeneca's premier global technology engine, leading digital clinical trial operations and life-sciences data science initiatives.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://www.astrazeneca.com/country-sites/india.html",
        "source_id": "company-newsrooms",
        "source_name": "AstraZeneca India Official Portal",
        "last_verified_date": "2024-08-20",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "paypal-india",
        "name": "PayPal India Technology Centre",
        "parent_company": "PayPal Holdings, Inc.",
        "hq_country": "United States",
        "city_id": "chennai",
        "city_name": "Chennai",
        "sector": "BFSI / Fintech",
        "year_established": 2006,
        "business_functions": "Real-Time Payment Risk Engines, Machine Learning Fraud Detection, Merchant Checkout SDKs, Compliance Automation",
        "short_description": "Houses significant technology and product engineering operations across Chennai and Bengaluru responsible for global transaction safety.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://newsroom.in.paypal-corp.com/",
        "source_id": "company-newsrooms",
        "source_name": "PayPal India Newsroom",
        "last_verified_date": "2024-08-27",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "intel-india",
        "name": "Intel India Development Center",
        "parent_company": "Intel Corporation",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Semiconductors & Electronics",
        "year_established": 1998,
        "business_functions": "SoC Architecture Design, Silicon Post-Silicon Validation, High-Performance Graphics Drivers, Xeon Server Microcode",
        "short_description": "Intel's largest design and development center outside the United States, advancing microprocessor architecture and 5G computing.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.intel.in/content/www/in/en/company-overview/intel-in-india.html",
        "source_id": "company-newsrooms",
        "source_name": "Intel in India Corporate Overview",
        "last_verified_date": "2024-09-09",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "qualcomm-india",
        "name": "Qualcomm India Development Center",
        "parent_company": "Qualcomm Incorporated",
        "hq_country": "United States",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "Semiconductors & Electronics",
        "year_established": 2004,
        "business_functions": "5G & 6G Modem Firmware, Snapdragon Neural Processing SDK, Automotive Cockpit Software, RF Front-End Architecture",
        "short_description": "Plays a vital role in Snapdragon chipset engineering and wireless protocols, recently inaugurating a major new facility in Hyderabad.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.qualcomm.com/company/locations/india",
        "source_id": "company-newsrooms",
        "source_name": "Qualcomm Worldwide Locations - India",
        "last_verified_date": "2024-09-17",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "cisco-globalization",
        "name": "Cisco Systems Globalization Centre",
        "parent_company": "Cisco Systems, Inc.",
        "hq_country": "United States",
        "city_id": "bengaluru",
        "city_name": "Bengaluru",
        "sector": "Technology & Software",
        "year_established": 1995,
        "business_functions": "Core Routing Operating Systems (IOS XR), Webex Real-Time Media Engines, Zero Trust Cybersecurity, Silicon Photonics",
        "short_description": "Established as Cisco's Globalization Centre East; houses major hardware and software engineering labs driving core enterprise networking.",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://www.cisco.com/c/en_in/about/cisco-in-india.html",
        "source_id": "company-newsrooms",
        "source_name": "Cisco in India Corporate Portal",
        "last_verified_date": "2024-09-01",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "pepsico-gbs",
        "name": "PepsiCo Global Business Services",
        "parent_company": "PepsiCo, Inc.",
        "hq_country": "United States",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "Retail & Consumer Tech",
        "year_established": 2019,
        "business_functions": "Global Demand Forecasting AI, Supply Chain Logistics Digital Twin, Precision Digital Marketing, Trade Spend Optimization",
        "short_description": "Strategic shared services and analytics nerve center supporting PepsiCo brands across North America, Europe, and Latin America.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://www.pepsico.com/who-we-are/global-locations",
        "source_id": "company-newsrooms",
        "source_name": "PepsiCo Global Operations Locations",
        "last_verified_date": "2024-08-16",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "novartis-corporate-center",
        "name": "Novartis Corporate Center Hyderabad",
        "parent_company": "Novartis AG",
        "hq_country": "Switzerland",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "Healthcare & Pharma",
        "year_established": 2007,
        "business_functions": "Biostatistics & Clinical Programming, Pharmacovigilance Case Processing, Commercial Data Science, Regulatory Affairs Filings",
        "short_description": "One of Novartis' primary global service centers; provides end-to-end clinical trial data management and global regulatory submissions.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.novartis.com/in-en/about/novartis-india",
        "source_id": "company-newsrooms",
        "source_name": "Novartis in India Official Portal",
        "last_verified_date": "2024-08-22",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "bristol-myers-squibb",
        "name": "Bristol Myers Squibb Hyderabad Centre",
        "parent_company": "Bristol Myers Squibb Company",
        "hq_country": "United States",
        "city_id": "hyderabad",
        "city_name": "Hyderabad",
        "sector": "Healthcare & Pharma",
        "year_established": 2023,
        "business_functions": "Drug Development Informatics, Molecular Screening AI, Global Clinical Operations, Enterprise IT Modernization",
        "short_description": "State-of-the-art facility launched with an investment exceeding $100M to expand global drug development capacity and digital innovation.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://www.bms.com/about-us/our-company/worldwide-facilities/india.html",
        "source_id": "company-newsrooms",
        "source_name": "Bristol Myers Squibb Worldwide Facilities",
        "last_verified_date": "2024-09-22",
        "verification_status": "Verified",
        "expansion_status": "Recently Launched"
    },
    {
        "id": "american-express-gcc",
        "name": "American Express Global Capabilities",
        "parent_company": "American Express Company",
        "hq_country": "United States",
        "city_id": "gurugram",
        "city_name": "Gurugram",
        "sector": "BFSI / Fintech",
        "year_established": 1995,
        "business_functions": "Credit Risk Machine Learning, Cardmember Fraud Prevention, Loyalty Rewards Platforms, Global Financial Settlement",
        "short_description": "Anchors American Express' largest proprietary corporate campus globally (nearly 1 million sq ft at Sector 74A Gurugram).",
        "headcount_bracket": "10,000+",
        "evidence_url": "https://about.americanexpress.com/who-we-are/global-locations/default.aspx",
        "source_id": "company-newsrooms",
        "source_name": "American Express Global Locations",
        "last_verified_date": "2024-09-25",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "fidelity-international-gurugram",
        "name": "Fidelity International Gurugram",
        "parent_company": "FIL Limited",
        "hq_country": "United Kingdom",
        "city_id": "gurugram",
        "city_name": "Gurugram",
        "sector": "BFSI / Fintech",
        "year_established": 2001,
        "business_functions": "Global Investment Management Tech, Portfolio Modeling Platforms, Enterprise Cyber Security, ESG Research Analytics",
        "short_description": "Delivers core technology and asset management operations supporting investors across Europe, Asia-Pacific, and the Middle East.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://www.fidelityrecruitment.com/india",
        "source_id": "company-newsrooms",
        "source_name": "Fidelity International India Portal",
        "last_verified_date": "2024-08-14",
        "verification_status": "Verified",
        "expansion_status": "Mature Operations"
    },
    {
        "id": "samsung-sri-noida",
        "name": "Samsung R&D Institute India (SRI-Noida)",
        "parent_company": "Samsung Electronics Co., Ltd.",
        "hq_country": "South Korea",
        "city_id": "noida",
        "city_name": "Noida",
        "sector": "Semiconductors & Electronics",
        "year_established": 2007,
        "business_functions": "Galaxy Smartphone Firmware, 5G Communication Protocol Stacks, Computational Camera AI, SmartThings IoT Integration",
        "short_description": "One of Samsung's primary software research hubs outside Korea, driving key camera AI algorithms and telecom network protocols.",
        "headcount_bracket": "1,000 - 5,000",
        "evidence_url": "https://research.samsung.com/sri-n",
        "source_id": "company-newsrooms",
        "source_name": "Samsung Research Institute Noida",
        "last_verified_date": "2024-09-19",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    },
    {
        "id": "adobe-india-dc",
        "name": "Adobe Systems India Development Centre",
        "parent_company": "Adobe Inc.",
        "hq_country": "United States",
        "city_id": "noida",
        "city_name": "Noida",
        "sector": "Technology & Software",
        "year_established": 1997,
        "business_functions": "Document Cloud & Acrobat Core, Creative Cloud Core Libraries, Firefly Generative AI Research, Experience Platform APIs",
        "short_description": "One of Adobe's largest R&D centers globally, with landmark towers in Noida and Bengaluru driving core algorithmic development.",
        "headcount_bracket": "5,000 - 10,000",
        "evidence_url": "https://www.adobe.com/about-adobe/contact/offices.html",
        "source_id": "company-newsrooms",
        "source_name": "Adobe Global Offices Directory",
        "last_verified_date": "2024-09-21",
        "verification_status": "Verified",
        "expansion_status": "Active & Expanding"
    }
]

EXPANSIONS = [
    {
        "id": "exp-1",
        "company_name": "American Express",
        "city_name": "Gurugram",
        "announcement_title": "Opens landmark 1-million-sq-ft green campus in Gurugram",
        "date": "2024-04-22",
        "details": "Inaugurated a state-of-the-art facility at Sector 74A Gurugram designed with platinum LEED environmental standards to house enterprise capabilities and AI risk teams.",
        "source_url": "https://about.americanexpress.com/newsroom/press-releases/default.aspx",
        "source_name": "American Express Corporate Newsroom"
    },
    {
        "id": "exp-2",
        "company_name": "Bristol Myers Squibb",
        "city_name": "Hyderabad",
        "announcement_title": "Invests $100M+ in next-generation Hyderabad Innovation Center",
        "date": "2023-10-18",
        "details": "Expanded science and technology capacity with a major multi-story facility in Hyderabad dedicated to AI molecular screening and clinical trials.",
        "source_url": "https://www.bms.com/about-us/our-company/worldwide-facilities/india.html",
        "source_name": "Bristol Myers Squibb Media Center"
    },
    {
        "id": "exp-3",
        "company_name": "Boeing",
        "city_name": "Bengaluru",
        "announcement_title": "Inaugurates 43-acre BIETC campus at Bengaluru Aerospace Park",
        "date": "2024-01-19",
        "details": "Opened Boeing's largest engineering investment outside the United States (~₹1,600 Cr investment) to pioneer avionics and flight deck software.",
        "source_url": "https://www.boeing.co.in/boeing-in-india/engineering-and-technology.page",
        "source_name": "Boeing India News"
    },
    {
        "id": "exp-4",
        "company_name": "Qualcomm",
        "city_name": "Hyderabad",
        "announcement_title": "Expands Hyderabad design facility for 5G & automotive silicon",
        "date": "2023-11-05",
        "details": "Leased additional Grade A office space at Rayadurgam to scale engineers working on Snapdragon automotive platforms and Wi-Fi 7 firmware.",
        "source_url": "https://www.qualcomm.com/company/locations/india",
        "source_name": "Qualcomm Press Office"
    },
    {
        "id": "exp-5",
        "company_name": "Standard Chartered",
        "city_name": "Chennai",
        "announcement_title": "Consolidates GBS operations into DLF Cybercity Chennai campus",
        "date": "2024-02-14",
        "details": "Expanded global trade finance engineering and client operations with expanded campus capacity in Chennai to support European and Asian markets.",
        "source_url": "https://www.sc.com/en/about/our-locations/india/",
        "source_name": "Standard Chartered Media Relations"
    }
]


def init_db(db_path: Path = DB_FILE, schema_path: Path = SCHEMA_FILE) -> sqlite3.Connection:
    """Initialize the SQLite database with schema and seed data."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Apply schema
    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # Insert sources
    for src in SOURCES:
        cursor.execute(
            """INSERT INTO sources (id, name, url, category, description, last_checked_date, reliability_tier)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (src["id"], src["name"], src["url"], src["category"], src["description"], src["last_checked_date"], src["reliability_tier"])
        )

    # Insert cities
    for c in CITIES:
        cursor.execute(
            """INSERT INTO cities (
                id, name, state, tier, indicative_rent_min, indicative_rent_max, indicative_rent_period,
                indicative_salary_entry_lakh, indicative_salary_mid_lakh, indicative_salary_senior_lakh,
                salary_benchmark_period, state_incentives, talent_ecosystem, infrastructure_notes,
                tradeoff_pros, tradeoff_cons, source_id, source_url, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                c["id"], c["name"], c["state"], c["tier"], c["indicative_rent_min"], c["indicative_rent_max"],
                c["indicative_rent_period"], c["indicative_salary_entry_lakh"], c["indicative_salary_mid_lakh"],
                c["indicative_salary_senior_lakh"], c["salary_benchmark_period"], c["state_incentives"],
                c["talent_ecosystem"], c["infrastructure_notes"], c["tradeoff_pros"], c["tradeoff_cons"],
                c["source_id"], c["source_url"], c["last_updated"]
            )
        )

    # Insert companies
    for comp in COMPANIES:
        cursor.execute(
            """INSERT INTO companies (
                id, name, parent_company, hq_country, city_id, city_name, sector,
                year_established, business_functions, short_description, headcount_bracket,
                evidence_url, source_id, source_name, last_verified_date, verification_status, expansion_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                comp["id"], comp["name"], comp["parent_company"], comp["hq_country"], comp["city_id"],
                comp["city_name"], comp["sector"], comp["year_established"], comp["business_functions"],
                comp["short_description"], comp["headcount_bracket"], comp["evidence_url"],
                comp["source_id"], comp["source_name"], comp["last_verified_date"], comp["verification_status"],
                comp["expansion_status"]
            )
        )

    # Insert expansions
    for exp in EXPANSIONS:
        cursor.execute(
            """INSERT INTO expansions (id, company_name, city_name, announcement_title, date, details, source_url, source_name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (exp["id"], exp["company_name"], exp["city_name"], exp["announcement_title"], exp["date"], exp["details"], exp["source_url"], exp["source_name"])
        )

    conn.commit()
    return conn


if __name__ == "__main__":
    print(f"Initializing database at: {DB_FILE}")
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM companies")
    comp_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM cities")
    city_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM sources")
    src_count = c.fetchone()[0]
    conn.close()
    print(f"Database initialized successfully! Seeded {comp_count} companies, {city_count} cities, {src_count} sources.")
