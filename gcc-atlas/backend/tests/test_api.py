"""
Comprehensive backend API tests for GCC Atlas
Tests health, dashboard KPIs, company filtering, city comparison, sources, and AI assistant.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure backend directory is in python path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify system health and database connectivity."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert data["total_companies"] >= 28
    assert data["total_cities"] >= 6


def test_dashboard_endpoint():
    """Verify dynamic dashboard calculation."""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_companies"] >= 28
    assert data["total_cities"] >= 6
    assert data["total_sectors"] >= 5
    assert len(data["sector_distribution"]) > 0
    assert len(data["city_distribution"]) > 0
    assert len(data["recent_companies"]) > 0
    assert len(data["recent_expansions"]) > 0
    assert "prototype_disclaimer" in data


def test_companies_list_and_search():
    """Verify company directory filtering, search, and pagination."""
    # List all
    res = client.get("/api/companies?page=1&limit=10")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 28
    assert len(data["items"]) == 10
    assert data["total_pages"] >= 3

    # Search for "Google"
    res_search = client.get("/api/companies?search=Google")
    assert res_search.status_code == 200
    search_data = res_search.json()
    assert search_data["total"] >= 1
    assert any("Google" in item["name"] for item in search_data["items"])

    # Filter by city "Noida"
    res_city = client.get("/api/companies?city=Noida")
    assert res_city.status_code == 200
    city_data = res_city.json()
    assert city_data["total"] >= 2
    for item in city_data["items"]:
        assert item["city_name"] == "Noida"

    # Filter by sector "BFSI / Fintech"
    res_sector = client.get("/api/companies?sector=BFSI%20%2F%20Fintech")
    assert res_sector.status_code == 200
    sector_data = res_sector.json()
    assert sector_data["total"] >= 5
    for item in sector_data["items"]:
        assert item["sector"] == "BFSI / Fintech"


def test_company_detail_and_404():
    """Verify single company profile retrieval and error handling."""
    res = client.get("/api/companies/microsoft-idc")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Microsoft India Development Center (IDC)"
    assert data["city_name"] == "Hyderabad"
    assert data["verification_status"] == "Verified"
    assert "Copilot" in data["business_functions"] or "Azure" in data["business_functions"]

    # Non-existent company
    res_404 = client.get("/api/companies/fake-nonexistent-company-xyz")
    assert res_404.status_code == 404


def test_cities_and_comparison():
    """Verify city listing and side-by-side comparison matrix."""
    # List cities
    res = client.get("/api/cities")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 6
    assert any(c["id"] == "bengaluru" for c in data["items"])

    # Compare 2 cities (Bengaluru and Hyderabad)
    res_cmp = client.get("/api/cities/compare?city_ids=bengaluru,hyderabad")
    assert res_cmp.status_code == 200
    cmp_data = res_cmp.json()
    assert len(cmp_data["compared_cities"]) == 2
    assert "tradeoff_analysis" in cmp_data
    assert "cost_leader" in cmp_data["tradeoff_analysis"]
    assert "summary_text" in cmp_data["tradeoff_analysis"]

    # Compare error when less than 2 cities
    res_err = client.get("/api/cities/compare?city_ids=bengaluru")
    assert res_err.status_code == 400


def test_sources_and_data_quality():
    """Verify sources registry and data quality completeness report."""
    res = client.get("/api/sources")
    assert res.status_code == 200
    data = res.json()
    assert data["total_sources"] >= 10
    assert "quality_metrics" in data
    assert data["quality_metrics"]["year_established_completeness_pct"] > 80.0
    assert data["quality_metrics"]["evidence_url_completeness_pct"] == 100.0


def test_ai_assistant_chat_in_demo_mode():
    """Verify conversational AI research assistant grounded responses and demo mode fallback."""
    # Query 1: Noida GCCs
    payload = {"message": "Which companies in the dataset have GCCs in Noida?"}
    res = client.post("/api/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Samsung" in data["answer"] or "Adobe" in data["answer"]
    assert len(data["citations"]) > 0
    assert data["is_demo_mode"] is True  # In test environment without key
    assert "DEMO MODE" in data["mode_badge"]

    # Query 2: Compare Hyderabad and Pune
    payload2 = {"message": "Compare Hyderabad and Pune for a technology GCC."}
    res2 = client.post("/api/assistant/chat", json=payload2)
    assert res2.status_code == 200
    data2 = res2.json()
    assert "Hyderabad" in data2["answer"] and "Pune" in data2["answer"]

    # Query 3: GCC setup checklist
    payload3 = {"message": "What information should a company gather before setting up a GCC in India?"}
    res3 = client.post("/api/assistant/chat", json=payload3)
    assert res3.status_code == 200
    data3 = res3.json()
    assert "Real Estate" in data3["answer"] or "Location" in data3["answer"]
