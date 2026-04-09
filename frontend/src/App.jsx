import { useState, useEffect, useCallback } from 'react'
import {
  getStats, getByCategory, getByType,
  getOverTime, getTopCompanies, getLatestJobs
} from './services/api'
import KPICards       from './components/KPICards'
import CategoryChart  from './components/CategoryChart'
import JobTypeChart   from './components/JobTypeChart'
import TimelineChart  from './components/TimelineChart'
import TopCompanies   from './components/TopCompanies'
import LatestJobs     from './components/LatestJobs'
import PipelineButton from './components/PipelineButton'
import './global.css'

export default function App() {
  const [stats,      setStats]      = useState(null)
  const [categories, setCategories] = useState([])
  const [jobTypes,   setJobTypes]   = useState([])
  const [timeline,   setTimeline]   = useState([])
  const [companies,  setCompanies]  = useState([])
  const [jobs,       setJobs]       = useState([])
  const [loading,    setLoading]    = useState(true)
  const [error,      setError]      = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchAll = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [s, cat, typ, time, comp, latest] = await Promise.all([
        getStats(),
        getByCategory(),
        getByType(),
        getOverTime(),
        getTopCompanies(),
        getLatestJobs(30),
      ])
      setStats(s.data)
      setCategories(cat.data)
      setJobTypes(typ.data)
      setTimeline(time.data)
      setCompanies(comp.data)
      setJobs(latest.data)
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (err) {
      setError('Could not connect to the backend. Make sure Flask is running on port 5000.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchAll() }, [fetchAll])

  return (
    <div className="min-h-screen bg-dark text-slate-200">

      {/* ── HEADER ─────────────────────────────── */}
      <header className="border-b border-border px-6 py-4 flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <span className="text-accent">◈</span>
            Remote Jobs Analytics
          </h1>
          <p className="text-xs text-slate-500 mt-0.5 font-mono">
            End-to-End Data Pipeline · Python ETL + Flask + React
          </p>
        </div>
        <div className="flex items-center gap-4">
          {lastUpdated && (
            <span className="text-xs text-slate-500 font-mono hidden sm:block">
              Last refreshed: {lastUpdated}
            </span>
          )}
          <PipelineButton onSuccess={fetchAll} />
          <button
            onClick={fetchAll}
            className="text-sm text-slate-400 hover:text-white border border-border px-3 py-2 rounded-lg transition-colors"
          >
            ↻ Refresh
          </button>
        </div>
      </header>

      {/* ── ERROR BANNER ───────────────────────── */}
      {error && (
        <div className="mx-6 mt-4 bg-red-900/40 border border-red-700 text-red-300 rounded-lg px-4 py-3 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* ── MAIN CONTENT ───────────────────────── */}
      <main className="p-6 space-y-6 max-w-screen-2xl mx-auto">

        {/* KPIs */}
        <KPICards stats={stats} loading={loading} />

        {/* Charts row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <CategoryChart data={categories} loading={loading} />
          </div>
          <div>
            <JobTypeChart data={jobTypes} loading={loading} />
          </div>
        </div>

        {/* Charts row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <TimelineChart data={timeline} loading={loading} />
          </div>
          <div>
            <TopCompanies data={companies} loading={loading} />
          </div>
        </div>

        {/* Jobs table */}
        <LatestJobs data={jobs} loading={loading} />

      </main>

      {/* ── FOOTER ─────────────────────────────── */}
      <footer className="border-t border-border px-6 py-4 text-center text-xs text-slate-600 font-mono">
        Built by R. Siraddeen · Data source: Remotive API · Stack: Python · Flask · PostgreSQL · React
      </footer>

    </div>
  )
}
