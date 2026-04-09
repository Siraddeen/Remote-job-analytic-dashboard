# 🔄 Remote Jobs Data Pipeline & Analytics Dashboard

An end-to-end data engineering project built to demonstrate
industry-level data pipeline concepts — from raw API ingestion
to a live analytics dashboard.

**Built by R. Siraddeen**

---

## 🏗️ Architecture

```
Remotive API (remote jobs data)
        ↓
Python ETL Pipeline
  ├── ingest.py    → Fetch raw JSON from API
  ├── transform.py → Clean with pandas (ETL Transform)
  └── load.py      → Insert into DB (idempotent)
        ↓
Database (SQLite locally / PostgreSQL in production)
        ↓
SQL Analytics Queries (db/analytics.py)
        ↓
Flask REST API (api/app.py)
        ↓
React Dashboard (frontend/)
  ├── KPI Summary Cards
  ├── Jobs by Category (Bar Chart)
  ├── Job Type Distribution (Pie Chart)
  ├── Jobs Over Time (Area Chart)
  ├── Top Companies (Leaderboard)
  └── Latest Jobs (Feed Table)
        ↓
Deployment: Render (Flask) + Vercel (React)
```

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| ETL        | Python, pandas, requests          |
| Database   | SQLite (dev) / PostgreSQL (prod)  |
| Backend    | Flask, flask-cors                 |
| Frontend   | React, Vite, Tailwind CSS         |
| Charts     | Recharts                          |
| HTTP       | Axios                             |
| Deployment | Render (backend), Vercel (frontend)|

---

## 🚀 Quick Start (Local)

### Step 1 — Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env
```

### Step 2 — Run ETL Pipeline (fetches data + loads DB)

```bash
# From the backend/ directory, with venv active:
python -m etl.pipeline
```

You should see:
```
🚀 DATA PIPELINE STARTED
[1/3] EXTRACT — Fetching from API...
✅ Fetched 150 jobs from API
[2/3] TRANSFORM — Cleaning data...
[3/3] LOAD — Inserting into database...
✅ PIPELINE COMPLETE
```

### Step 3 — Start Flask API

```bash
# Still in backend/, venv active:
python -m api.app
```

API running at: http://localhost:5000

Test it:
```
http://localhost:5000/api/health
http://localhost:5000/api/stats
http://localhost:5000/api/jobs/by-category
```

### Step 4 — Start React Frontend

```bash
# In a NEW terminal:
cd frontend
npm install
npm run dev
```

Dashboard at: http://localhost:5173

---

## 📡 API Endpoints

| Method | Endpoint                  | Description               |
|--------|---------------------------|---------------------------|
| GET    | /api/health               | Health check              |
| GET    | /api/pipeline/run         | Trigger ETL pipeline      |
| GET    | /api/stats                | KPI summary (4 metrics)   |
| GET    | /api/jobs/by-category     | Jobs grouped by category  |
| GET    | /api/jobs/by-type         | Jobs grouped by type      |
| GET    | /api/jobs/over-time       | Daily job counts (30 days)|
| GET    | /api/jobs/top-companies   | Top 10 hiring companies   |
| GET    | /api/jobs/latest?limit=20 | Most recent job listings  |

---

## ☁️ Deployment

### Backend → Render

1. Push `backend/` to a GitHub repo
2. Go to render.com → New Web Service
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn api.app:app`
5. Add environment variables:
   - `DB_TYPE` = `postgresql`
   - `DATABASE_URL` = (your Railway/Render PostgreSQL URL)

### Database → Railway or Render PostgreSQL

1. Go to railway.app → New → PostgreSQL
2. Copy the `DATABASE_URL` from the connect tab
3. Add it as an env variable in your Render backend

### Frontend → Vercel

1. Push `frontend/` to GitHub
2. Go to vercel.com → Import Project
3. Add environment variable:
   - `VITE_API_URL` = your Render backend URL (e.g. `https://yourapp.onrender.com`)
4. Deploy

---

## 📁 Project Structure

```
data-pipeline/
├── backend/
│   ├── api/
│   │   └── app.py              ← Flask REST API
│   ├── db/
│   │   ├── connection.py       ← DB connection (SQLite/PostgreSQL)
│   │   ├── schema.py           ← Table creation + indexes
│   │   └── analytics.py        ← SQL analytics queries
│   ├── etl/
│   │   ├── ingest.py           ← Extract: fetch from API
│   │   ├── transform.py        ← Transform: clean with pandas
│   │   ├── load.py             ← Load: insert into DB
│   │   └── pipeline.py         ← Orchestrator (runs E→T→L)
│   ├── data/                   ← Auto-created: raw + cleaned CSVs
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── KPICards.jsx
│   │   │   ├── CategoryChart.jsx
│   │   │   ├── JobTypeChart.jsx
│   │   │   ├── TimelineChart.jsx
│   │   │   ├── TopCompanies.jsx
│   │   │   ├── LatestJobs.jsx
│   │   │   └── PipelineButton.jsx
│   │   ├── services/
│   │   │   └── api.js          ← All API calls
│   │   ├── App.jsx             ← Main dashboard layout
│   │   ├── main.jsx
│   │   └── global.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
└── README.md
```

---

## 🧠 Key Concepts (for interviews)

**ETL Pipeline:**
Extract → Transform → Load. Each stage is isolated so
failures don't cascade and stages can be re-run independently.

**Idempotent Inserts:**
Running the pipeline multiple times won't create duplicate
records. We use `INSERT OR IGNORE` (SQLite) / `ON CONFLICT DO NOTHING` (PostgreSQL).

**Indexes:**
We index `category` and `job_type` columns — this makes
GROUP BY queries much faster on large datasets.

**API Layer:**
The Flask API decouples the database from the frontend.
The React app never talks directly to the DB — only through the API.

**Data Quality:**
Transform stage checks for nulls, duplicates, and inconsistent
formatting before anything reaches the database.
