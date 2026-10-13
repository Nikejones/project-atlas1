"""
Vercel Serverless Entrypoint for GCC Atlas
Exposes ASGI FastAPI app instance for Vercel Python runtime.
"""

import sys
import os
from pathlib import Path

# Setup paths for Vercel serverless environment
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import main application
from app.main import app

# Vercel entrypoint
handler = app
