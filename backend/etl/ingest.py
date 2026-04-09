"""
etl/ingest.py
─────────────────────────────────────────────────
PHASE: Extract (E in ETL)

This module fetches raw data from the Remotive API.

What is ETL?
  Extract  → Pull raw data from a source (API, CSV, DB)
  Transform → Clean, reshape, validate the data
  Load     → Insert into target database

Why separate ingestion from transformation?
  In production pipelines (AWS Glue, Apache Airflow),
  each step is isolated so you can re-run any stage
  independently if something fails.
"""

import requests
import json
import os

API_URL = "https://remotive.com/api/remote-jobs"
RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw_jobs.json")


def fetch_jobs(limit=100):
    """
    Fetches remote jobs from the Remotive API.
    Returns raw list of job dicts.
    """
    print(f"📡 Fetching jobs from {API_URL} ...")

    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()  # raises exception for 4xx/5xx
    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Loading from local cache if available...")
        return _load_from_cache()
    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
        return []

    data = response.json()
    jobs = data.get("jobs", [])

    print(f"✅ Fetched {len(jobs)} jobs from API.")

    # Save raw data as cache
    _save_to_cache(jobs)

    return jobs[:limit]


def _save_to_cache(jobs):
    """Save raw API response to a local JSON file as backup."""
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    with open(RAW_DATA_PATH, "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"💾 Raw data cached at {RAW_DATA_PATH}")


def _load_from_cache():
    """Load data from local cache if API is unavailable."""
    if os.path.exists(RAW_DATA_PATH):
        with open(RAW_DATA_PATH, "r") as f:
            jobs = json.load(f)
        print(f"📂 Loaded {len(jobs)} jobs from local cache.")
        return jobs
    print("⚠️  No cache found. Cannot proceed.")
    return []


def inspect_sample(jobs, n=2):
    """
    Print a few job records so you understand the raw structure.
    Useful during development.
    """
    print("\n─── Sample Raw Job Record ───")
    for job in jobs[:n]:
        print(json.dumps({k: job.get(k) for k in [
            "id", "title", "company_name", "category",
            "job_type", "publication_date", "url", "salary",
            "tags", "description"
        ]}, indent=2))


if __name__ == "__main__":
    jobs = fetch_jobs(limit=200)
    inspect_sample(jobs)
