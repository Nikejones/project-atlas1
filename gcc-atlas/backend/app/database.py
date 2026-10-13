"""
Database helper and connection management for GCC Atlas
"""

import sqlite3
from typing import Generator, Dict, Any, List, Optional
from contextlib import contextmanager
from app.config import settings


import os
import shutil
from pathlib import Path


def get_effective_db_path() -> Path:
    """Return writable database path, copying to /tmp in serverless environments like Vercel."""
    target = settings.db_path
    if os.getenv("VERCEL") or (target.exists() and not os.access(target.parent, os.W_OK)):
        tmp_db = Path("/tmp/gcc_atlas.db")
        if not tmp_db.exists() and target.exists():
            try:
                shutil.copy2(target, tmp_db)
            except Exception as e:
                print(f"Warning: Could not copy DB to /tmp: {e}")
        if tmp_db.exists():
            return tmp_db
    return target


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite database connection."""
    conn = sqlite3.connect(get_effective_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def query_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute query and return list of dictionaries."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def query_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """Execute query and return single dictionary or None."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None


def execute_write(query: str, params: tuple = ()) -> int:
    """Execute write statement and return lastrowid."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid or 0
