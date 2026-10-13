"""
GCC Atlas Local Server Runner
Starts the FastAPI application and serves both the REST API and the frontend.
"""

import sys
import os
from pathlib import Path
import uvicorn

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from backend.data.seed_data import init_db, DB_FILE

if __name__ == "__main__":
    # Ensure database is seeded
    if not DB_FILE.exists():
        print(f"[*] Initializing database at {DB_FILE}...")
        init_db(DB_FILE)
    else:
        print(f"[*] Found existing database at {DB_FILE}")

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

    print("=" * 60)
    print(" GCC Atlas — AI-Powered GCC Intelligence Platform")
    print(f" Web Application: http://{host}:{port}")
    print(f" Swagger API Docs: http://{host}:{port}/docs")
    print("=" * 60)

    uvicorn.run("app.main:app", host=host, port=port, reload=False, app_dir=str(backend_dir))
