"""
GCC Atlas FastAPI Main Application
Serves REST API routes and static frontend files.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes.health import router as health_router
from app.routes.dashboard import router as dashboard_router
from app.routes.companies import router as companies_router
from app.routes.cities import router as cities_router
from app.routes.sources import router as sources_router
from app.routes.assistant import router as assistant_router
from data.seed_data import init_db

# Ensure database exists
if not settings.db_path.exists():
    try:
        print(f"Database not found at {settings.db_path}. Initializing with seed data...")
        init_db(settings.db_path)
    except Exception as e:
        print(f"Warning: Could not initialize database in current environment: {e}")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Enterprise GCC Intelligence Platform for multinational companies, consultants, and analysts.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers under /api
app.include_router(health_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(companies_router, prefix="/api")
app.include_router(cities_router, prefix="/api")
app.include_router(sources_router, prefix="/api")
app.include_router(assistant_router, prefix="/api")

# Serve frontend static assets
if settings.frontend_dir.exists():
    app.mount("/", StaticFiles(directory=settings.frontend_dir, html=True), name="frontend")
