"""
db/analytics.py
─────────────────────────────────────────────────
SQL ANALYTICS LAYER

These are the queries that power the dashboard.

In Data Engineering, analytics queries are the
"value layer" — they turn raw stored data into
business insights.

Each function:
  1. Connects to the DB
  2. Runs a specific SQL query
  3. Returns clean Python dict/list for the API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from db.connection import get_connection


def _fetchall_as_dicts(cursor, query, params=None):
    """Helper: runs query and returns list of dicts."""
    cursor.execute(query, params or [])
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def jobs_by_category():
    """
    How many job listings exist per category?
    Use case: Bar chart of top categories.
    """
    conn = get_connection()
    cursor = conn.cursor()
    results = _fetchall_as_dicts(cursor, """
        SELECT
            category,
            COUNT(*) AS job_count
        FROM jobs
        WHERE category IS NOT NULL
          AND category != ''
        GROUP BY category
        ORDER BY job_count DESC
        LIMIT 15;
    """)
    cursor.close()
    conn.close()
    return results


def jobs_by_type():
    """
    Distribution of full_time vs contract vs part_time etc.
    Use case: Pie / Donut chart.
    """
    conn = get_connection()
    cursor = conn.cursor()
    results = _fetchall_as_dicts(cursor, """
        SELECT
            job_type,
            COUNT(*) AS job_count
        FROM jobs
        WHERE job_type IS NOT NULL
          AND job_type != ''
        GROUP BY job_type
        ORDER BY job_count DESC;
    """)
    cursor.close()
    conn.close()
    return results


def jobs_over_time():
    """
    How many jobs were published per day?
    Use case: Line chart showing trend.
    """
    conn = get_connection()
    cursor = conn.cursor()
    results = _fetchall_as_dicts(cursor, """
        SELECT
            SUBSTR(publication_date, 1, 10) AS date,
            COUNT(*) AS job_count
        FROM jobs
        WHERE publication_date IS NOT NULL
          AND publication_date != ''
        GROUP BY SUBSTR(publication_date, 1, 10)
        ORDER BY date DESC
        LIMIT 30;
    """)
    cursor.close()
    conn.close()
    return results


def top_companies():
    """
    Which companies post the most remote jobs?
    Use case: Leaderboard table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    results = _fetchall_as_dicts(cursor, """
        SELECT
            company_name,
            COUNT(*) AS job_count
        FROM jobs
        WHERE company_name IS NOT NULL
          AND company_name != ''
          AND company_name != 'Unknown Company'
        GROUP BY company_name
        ORDER BY job_count DESC
        LIMIT 10;
    """)
    cursor.close()
    conn.close()
    return results


def latest_jobs(limit=20):
    """
    Fetch the most recently published jobs.
    Use case: Jobs feed table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    results = _fetchall_as_dicts(cursor, f"""
        SELECT
            job_id,
            title,
            company_name,
            category,
            job_type,
            publication_date,
            url,
            salary
        FROM jobs
        WHERE publication_date IS NOT NULL
        ORDER BY publication_date DESC
        LIMIT {int(limit)};
    """)
    cursor.close()
    conn.close()
    return results


def summary_stats():
    """
    High-level KPIs for the dashboard header.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs;")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT company_name) FROM jobs;")
    companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT category) FROM jobs;")
    categories = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM jobs
        WHERE CAST(SUBSTR(publication_date, 1, 10) AS DATE) = CURRENT_DATE;
    """)
    today = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_jobs": total,
        "total_companies": companies,
        "total_categories": categories,
        "jobs_today": today,
    }


if __name__ == "__main__":
    print("📊 Summary Stats:", summary_stats())
    print("\n📊 Jobs by Category:")
    for r in jobs_by_category():
        print(f"  {r['category']:30s} {r['job_count']}")
    print("\n📊 Jobs by Type:")
    for r in jobs_by_type():
        print(f"  {r['job_type']:20s} {r['job_count']}")
