/**
 * services/api.js
 * ─────────────────────────────────────────────
 * Central API service for the frontend.
 *
 * Why a service layer?
 *   Instead of writing axios.get(...) in every component,
 *   all API calls live here. If the backend URL changes,
 *   you update ONE file — nothing else breaks.
 */

import axios from "axios";

// In dev, Vite proxies /api → http://localhost:5000
// In production, set VITE_API_URL in your .env

// const BASE = import.meta.env.VITE_API_URL || ''
const BASE = "http://localhost:5000";

const api = axios.create({ baseURL: BASE });

export const getStats = () => api.get("/api/stats");
export const getByCategory = () => api.get("/api/jobs/by-category");
export const getByType = () => api.get("/api/jobs/by-type");
export const getOverTime = () => api.get("/api/jobs/over-time");
export const getTopCompanies = () => api.get("/api/jobs/top-companies");
export const getLatestJobs = (limit = 20) =>
  api.get(`/api/jobs/latest?limit=${limit}`);
export const runPipeline = () => api.get("/api/pipeline/run");
export const healthCheck = () => api.get("/api/health");
