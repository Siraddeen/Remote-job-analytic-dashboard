"""
db/schema.py
─────────────────────────────────────────────────
Creates the jobs table in the database.

In Data Engineering, schema design is critical.
A well-designed schema:
  - Avoids data redundancy
  - Makes queries fast (indexes)
  - Makes future changes easy

Our schema stores remote job listings with:
  - Unique job ID (prevents duplicate inserts)
  - Job metadata (title, company, category, type)
  - Dates (for time-based analytics)
  - Salary info (when available)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from db.connection import get_connection, is_postgres


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    if is_postgres():
        # PostgreSQL syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id              SERIAL PRIMARY KEY,
                job_id          INTEGER UNIQUE,
                title           TEXT NOT NULL,
                company_name    TEXT,
                category        TEXT,
                job_type        TEXT,
                publication_date TEXT,
                url             TEXT,
                salary          TEXT,
                tags            TEXT,
                ingested_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Index on category and job_type for fast GROUP BY queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_category
            ON jobs(category);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_type
            ON jobs(job_type);
        """)
    else:
        # SQLite syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id          INTEGER UNIQUE,
                title           TEXT NOT NULL,
                company_name    TEXT,
                category        TEXT,
                job_type        TEXT,
                publication_date TEXT,
                url             TEXT,
                salary          TEXT,
                tags            TEXT,
                ingested_at     TEXT DEFAULT (datetime('now'))
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_category
            ON jobs(category);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_type
            ON jobs(job_type);
        """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
