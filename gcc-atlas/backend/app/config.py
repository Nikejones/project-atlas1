"""
Application configuration for GCC Atlas
"""

import os
from pathlib import Path
from pydantic import BaseModel
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "gcc_atlas.db"
FRONTEND_DIR = BASE_DIR.parent / "frontend"


class Settings(BaseModel):
    app_name: str = "GCC Atlas — AI-Powered GCC Intelligence Platform"
    version: str = "1.0.0"
    db_path: Path = DB_PATH
    frontend_dir: Path = FRONTEND_DIR
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_timeout_seconds: float = 15.0
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
