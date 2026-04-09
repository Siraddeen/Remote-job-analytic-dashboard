"""
etl/transform.py
─────────────────────────────────────────────────
PHASE: Transform (T in ETL)

This module cleans and validates raw job data.

Why data cleaning matters:
  Real-world APIs send messy data:
  - Missing values (nulls)
  - Inconsistent formatting
  - Duplicate records
  - Irrelevant fields

  If you load dirty data into your DB, your analytics
  will be wrong. "Garbage in, garbage out."

Data Quality Checks we apply:
  1. Drop duplicates (by job_id)
  2. Fill missing values with meaningful defaults
  3. Normalize text (strip whitespace, lowercase categories)
  4. Parse and standardize dates
  5. Validate required fields exist
"""

import pandas as pd
import os
import re

CLEANED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_jobs.csv")


def transform(raw_jobs: list) -> pd.DataFrame:
    """
    Takes raw job list from API.
    Returns a clean pandas DataFrame ready for DB insertion.
    """
    if not raw_jobs:
        print("⚠️  No jobs to transform.")
        return pd.DataFrame()

    print(f"\n🔧 Transforming {len(raw_jobs)} raw job records...")

    # ── Step 1: Convert to DataFrame ────────────────────────
    df = pd.DataFrame(raw_jobs)
    print(f"   Raw columns: {list(df.columns)}")

    # ── Step 2: Select only relevant columns ─────────────────
    columns_needed = [
        "id", "title", "company_name", "category",
        "job_type", "publication_date", "url", "salary", "tags"
    ]
    # Only keep columns that actually exist in the response
    columns_present = [c for c in columns_needed if c in df.columns]
    df = df[columns_present].copy()

    # ── Step 3: Rename 'id' to 'job_id' to avoid DB conflict ─
    if "id" in df.columns:
        df.rename(columns={"id": "job_id"}, inplace=True)

    # ── Step 4: Handle missing values ────────────────────────
    df["title"]            = df["title"].fillna("Unknown Title").str.strip()
    df["company_name"]     = df["company_name"].fillna("Unknown Company").str.strip()
    df["category"]         = df["category"].fillna("Other").str.strip()
    df["job_type"]         = df["job_type"].fillna("full_time").str.strip()
    df["publication_date"] = df["publication_date"].fillna("").str.strip()
    df["url"]              = df["url"].fillna("").str.strip()
    df["salary"]           = df["salary"].fillna("Not disclosed").str.strip()

    # ── Step 5: Handle tags (list → comma-separated string) ──
    if "tags" in df.columns:
        df["tags"] = df["tags"].apply(
            lambda t: ", ".join(t) if isinstance(t, list) else str(t) if t else ""
        )
    else:
        df["tags"] = ""

    # ── Step 6: Normalize category (title case, strip extras) ─
    df["category"] = df["category"].str.title().str.strip()
    df["job_type"] = df["job_type"].str.lower().str.replace("-", "_").str.strip()

    # ── Step 7: Remove duplicates by job_id ──────────────────
    before = len(df)
    df.drop_duplicates(subset=["job_id"], keep="first", inplace=True)
    after = len(df)
    if before != after:
        print(f"   🗑️  Removed {before - after} duplicate records.")

    # ── Step 8: Drop rows missing critical fields ─────────────
    df.dropna(subset=["title"], inplace=True)
    df = df[df["title"] != ""]

    # ── Step 9: Data quality report ──────────────────────────
    print(f"\n📊 Data Quality Report:")
    print(f"   Records after cleaning : {len(df)}")
    print(f"   Columns                : {list(df.columns)}")
    print(f"   Null values remaining  :\n{df.isnull().sum()}")
    print(f"\n   Category distribution:\n{df['category'].value_counts().head(8).to_string()}")
    print(f"\n   Job type distribution:\n{df['job_type'].value_counts().to_string()}")

    # ── Step 10: Save cleaned CSV ─────────────────────────────
    os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"\n💾 Cleaned data saved to {CLEANED_DATA_PATH}")

    return df


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from etl.ingest import fetch_jobs
    raw = fetch_jobs(limit=200)
    df = transform(raw)
    print("\n✅ Sample cleaned data:")
    print(df.head(3).to_string())
