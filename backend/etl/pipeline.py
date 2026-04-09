"""
etl/pipeline.py
─────────────────────────────────────────────────
PIPELINE ORCHESTRATOR

This is the main entry point for the ETL pipeline.
It wires Extract → Transform → Load together.

In production (AWS), this would be triggered by:
  - AWS Glue Job
  - AWS Lambda + EventBridge (scheduled)
  - Apache Airflow DAG
  - GitHub Actions cron job

For now, you run it manually: python -m etl.pipeline
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
from etl.ingest import fetch_jobs
from etl.transform import transform
from etl.load import load


def run_pipeline(limit=200):
    start = time.time()
    print("=" * 55)
    print("  🚀 DATA PIPELINE STARTED")
    print("=" * 55)

    # ── EXTRACT ──────────────────────────────────────────────
    print("\n[1/3] EXTRACT — Fetching from API...")
    raw_jobs = fetch_jobs(limit=limit)

    if not raw_jobs:
        print("❌ Pipeline aborted: No data fetched.")
        return

    # ── TRANSFORM ─────────────────────────────────────────────
    print("\n[2/3] TRANSFORM — Cleaning data...")
    clean_df = transform(raw_jobs)

    if clean_df.empty:
        print("❌ Pipeline aborted: No clean data after transformation.")
        return

    # ── LOAD ──────────────────────────────────────────────────
    print("\n[3/3] LOAD — Inserting into database...")
    inserted = load(clean_df)

    elapsed = time.time() - start
    print("\n" + "=" * 55)
    print(f"  ✅ PIPELINE COMPLETE")
    print(f"     Records processed : {len(clean_df)}")
    print(f"     Records inserted  : {inserted}")
    print(f"     Duration          : {elapsed:.2f}s")
    print("=" * 55)


if __name__ == "__main__":
    run_pipeline()
