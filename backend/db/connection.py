"""
db/connection.py
─────────────────────────────────────────────────
Handles database connections.
- Local dev  → SQLite (zero setup, file-based)
- Production → PostgreSQL (Railway / Render)

Why this matters in Data Engineering:
  A proper connection module centralises all DB logic.
  If you switch from SQLite to PostgreSQL, you only
  change ONE file — nothing else in the project breaks.
"""

import os
import sqlite3
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DATABASE_URL = os.getenv("DATABASE_URL", "")
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "..", "jobs.db")


def get_connection():
    """
    Returns a database connection.
    Automatically uses SQLite or PostgreSQL based on .env
    """
    if DB_TYPE == "postgresql" and DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row  # enables dict-like row access
    return conn


def get_placeholder():
    """
    SQLite uses ? as placeholder, PostgreSQL uses %s
    Returns the correct one based on DB_TYPE.
    """
    return "%s" if (DB_TYPE == "postgresql" and DATABASE_URL) else "?"


def is_postgres():
    return DB_TYPE == "postgresql" and DATABASE_URL != ""
