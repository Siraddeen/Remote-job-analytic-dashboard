"""
api/app.py
─────────────────────────────────────────────────
FLASK REST API

This is the backend API that the React frontend
calls to get data for the dashboard.

Endpoints:
  GET /api/health              → health check
  GET /api/pipeline/run        → triggers ETL pipeline
  GET /api/stats               → KPI summary
  GET /api/jobs/by-category    → bar chart data
  GET /api/jobs/by-type        → pie chart data
  GET /api/jobs/over-time      → line chart data
  GET /api/jobs/top-companies  → leaderboard table
  GET /api/jobs/latest         → jobs feed

CORS is enabled so the React app (on a different port)
can call this API without browser security errors.
"""

import sys
import os

from flask_cors import CORS


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow React frontend to call this API
# CORS(app, resources={r"/*": {"origins": "*"}})

# ── Import analytics and pipeline ────────────────────────────
from db.analytics import (
    jobs_by_category,
    jobs_by_type,
    jobs_over_time,
    top_companies,
    latest_jobs,
    summary_stats,
)
from etl.pipeline import run_pipeline


# ── HEALTH CHECK ──────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "API is running ✅"})


# ── TRIGGER PIPELINE ──────────────────────────────────────────
@app.route("/api/pipeline/run")
def trigger_pipeline():
    """
    Manually triggers the ETL pipeline.
    In production this would be a POST with auth token.
    """
    try:
        run_pipeline(limit=200)
        return jsonify({"status": "success", "message": "Pipeline completed ✅"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ── SUMMARY STATS ─────────────────────────────────────────────
@app.route("/api/stats")
def get_stats():
    try:
        return jsonify(summary_stats())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── JOBS BY CATEGORY ─────────────────────────────────────────
@app.route("/api/jobs/by-category")
def get_by_category():
    try:
        return jsonify(jobs_by_category())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── JOBS BY TYPE ─────────────────────────────────────────────
@app.route("/api/jobs/by-type")
def get_by_type():
    try:
        return jsonify(jobs_by_type())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── JOBS OVER TIME ────────────────────────────────────────────
@app.route("/api/jobs/over-time")
def get_over_time():
    try:
        return jsonify(jobs_over_time())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── TOP COMPANIES ─────────────────────────────────────────────
@app.route("/api/jobs/top-companies")
def get_top_companies():
    try:
        return jsonify(top_companies())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── LATEST JOBS ───────────────────────────────────────────────
@app.route("/api/jobs/latest")
def get_latest():
    limit = request.args.get("limit", 20, type=int)
    try:
        return jsonify(latest_jobs(limit=limit))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# port = int(os.environ.get("PORT", 5000))
# app.run(host="0.0.0.0", port=port)A


# # ── ENTRY POINT ───────────────────────────────────────────────
# if __name__ == "__main__":
#     port = int(os.getenv("FLASK_PORT", 5000))
#     print(f"🚀 API running at http://localhost:{port}")
#     app.run(debug=True, port=port)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 API running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port)