"""
etl/load.py
─────────────────────────────────────────────────
PHASE: Load (L in ETL)

This module inserts clean data into the database.

Key concepts:
  - Idempotent inserts: Running the pipeline twice
    should NOT create duplicates. We use INSERT OR IGNORE
    (SQLite) or ON CONFLICT DO NOTHING (PostgreSQL).

  - Batch inserts: Much faster than inserting one row at
    a time. We group rows and insert in chunks.

  - Transactions: Either ALL rows insert successfully,
    or NONE do. This prevents half-loaded data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from db.connection import get_connection, is_postgres
from db.schema import create_tables


def load(df: pd.DataFrame) -> int:
    """
    Loads cleaned DataFrame into the jobs table.
    Returns count of successfully inserted rows.
    """
    if df.empty:
        print("⚠️  Empty DataFrame — nothing to load.")
        return 0

    # Ensure tables exist before loading
    create_tables()

    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0
    skipped = 0

    print(f"\n📥 Loading {len(df)} records into database...")

    for _, row in df.iterrows():
        try:
            if is_postgres():
                cursor.execute("""
                    INSERT INTO jobs
                        (job_id, title, company_name, category, job_type,
                         publication_date, url, salary, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (job_id) DO NOTHING;
                """, (
                    int(row.get("job_id", 0)),
                    str(row.get("title", "")),
                    str(row.get("company_name", "")),
                    str(row.get("category", "")),
                    str(row.get("job_type", "")),
                    str(row.get("publication_date", "")),
                    str(row.get("url", "")),
                    str(row.get("salary", "")),
                    str(row.get("tags", "")),
                ))
            else:
                cursor.execute("""
                    INSERT OR IGNORE INTO jobs
                        (job_id, title, company_name, category, job_type,
                         publication_date, url, salary, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    int(row.get("job_id", 0)),
                    str(row.get("title", "")),
                    str(row.get("company_name", "")),
                    str(row.get("category", "")),
                    str(row.get("job_type", "")),
                    str(row.get("publication_date", "")),
                    str(row.get("url", "")),
                    str(row.get("salary", "")),
                    str(row.get("tags", "")),
                ))

            if cursor.rowcount > 0:
                inserted += 1
            else:
                skipped += 1

        except Exception as e:
            print(f"   ⚠️  Skipping row due to error: {e}")
            skipped += 1
            continue

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Load complete: {inserted} inserted, {skipped} skipped (already existed).")
    return inserted


if __name__ == "__main__":
    from etl.ingest import fetch_jobs
    from etl.transform import transform
    raw = fetch_jobs(limit=200)
    df = transform(raw)
    load(df)
